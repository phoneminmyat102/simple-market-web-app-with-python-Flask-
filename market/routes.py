from market import app, render_template
from market.models import Item, User, db
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellingForm
from flask import redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseForm()
    selling_form = SellingForm()

    if request.method == 'POST':
        item_id = request.form.get('purchased_item')
        purchased_item = Item.query.filter_by(id=item_id).first()
        
        if purchased_item:
            if current_user.can_purchase(purchased_item):
                purchased_item.buy(current_user)
                flash(f"Congratulations! You purchased {purchased_item.name} for {purchased_item.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {purchased_item.name}!", category='danger')

    
        # selling owned items 
        sold_item_id = request.form.get('sold_item')
        selling_item = Item.query.filter_by(id=sold_item_id).first()
        if selling_item:
            if current_user.can_sell(selling_item):
                selling_item.sell(current_user)
                flash(f"Congratulations! You sold {selling_item.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {selling_item.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(name=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Success! New account has been created.You are logged in as : {user_to_create.name}', category='success')
        return redirect(url_for('market_page'))
    
    if form.errors != {}:
            for err_msgs in form.errors.values():
                for err_msg in err_msgs:
                    flash(f'Error: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correct(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.name}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again.',category='danger')

    if form.errors != {}:
        for err_msgs in form.errors.values():
            for err_msg in err_msgs:
                flash(f'Error: {err_msg}', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():

    logout_user()
    flash('You have been logged out successfully!', category='info')
    return redirect(url_for('home'))