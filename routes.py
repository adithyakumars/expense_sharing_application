from flask import request, jsonify, current_app
from models import User, Expense
from database import db
from schemas import UserSchema, ExpenseSchema
from auth import create_token, verify_token
from marshmallow import ValidationError
import json
from functools import wraps

def configure_routes(app):
    user_schema = UserSchema()
    expense_schema = ExpenseSchema()

    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                parts = auth_header.split(" ")
                if len(parts) == 2 and parts[0] == "Bearer":
                    token = parts[1]
                else:
                    current_app.logger.warning(f"Invalid Authorization header format: {auth_header}")
                    return jsonify({'message': 'Invalid Authorization header format'}), 401

            if not token:
                current_app.logger.warning("Token is missing")
                return jsonify({'message': 'Token is missing'}), 401

            try:
                claims = verify_token(token)
                if not claims:
                    raise ValueError('Token verification failed')
            except Exception as e:
                current_app.logger.error(f"Token verification error: {e}")
                return jsonify({'message': 'Token is invalid'}), 401
            return f(*args, **kwargs, email=claims['email'])
        return decorator

    @app.route('/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            user_data = user_schema.load(data)
            new_user = User(email=user_data['email'], name=user_data['name'], mobile_number=user_data['mobile_number'])
            new_user.set_password(user_data['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except ValidationError as err:
            return jsonify(err.messages), 400

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_token(user.email)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                'email': user.email,
                'name': user.name,
                'mobile_number': user.mobile_number
            }
            user_list.append(user_data)
        return jsonify(user_list)

    # @app.route('/expenses', methods=['POST'])
    # @token_required
    # def add_expense(email):
    #     try:
    #         data = request.get_json()
    #         user = User.query.filter_by(email=email).first()
    #         if not user:
    #             return jsonify({'message': 'User not found'}), 404
            
    #         expense_data = expense_schema.load(data, context={'split_method': data['split_method']})
    #         split_details = json.dumps(expense_data['split_details']) if 'split_details' in expense_data else None
    #         new_expense = Expense(description=expense_data['description'], amount=expense_data['amount'], split_method=expense_data['split_method'], user_id=user.id, split_details=split_details)
    #         db.session.add(new_expense)
    #         db.session.commit()
    #         return jsonify({'message': 'Expense added successfully'}), 201
    # except ValidationError as err:
    #         return jsonify(err.messages), 400

    # @app.route('/expenses', methods=['POST'])
    # def add_expense():
    #     data = request.get_json()
    #     user = User.query.filter_by(email=data['email']).first()
    #     if not user:
    #         return jsonify({'message': 'User not found'}), 404
        
    #     split_details = json.dumps(data['split_details']) if data['split_details'] else None
    #     new_expense = Expense(description=data['description'], amount=data['amount'], split_method=data['split_method'], user_id=user.id, split_details=split_details)
    #     db.session.add(new_expense)
    #     db.session.commit()
    #     return jsonify({'message': 'Expense added successfully'}), 201

    @app.route('/expenses', methods=['POST'])
    @token_required
    def add_expense(email):
        try:
            data = request.get_json()
            # No need to fetch user by email from data
            user = User.query.filter_by(email=email).first()  # Use the email from the token
        
            if not user:
                return jsonify({'message': 'User not found'}), 404

                split_details = json.dumps(data['split_details']) if 'split_details' in data else None
        
            new_expense = Expense(
                description=data['description'],
                amount=data['amount'],
                split_method=data['split_method'],
                user_id=user.id,
                split_details=split_details
            )
        
            db.session.add(new_expense)
            db.session.commit()
            return jsonify({'message': 'Expense added successfully'}), 201
        except KeyError as e:
            return jsonify({'message': f'Missing key: {str(e)}'}), 400
        except ValidationError as err:
             return jsonify(err.messages), 400
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500


    @app.route('/users/<email>/expenses', methods=['GET'])
    @token_required
    def get_user_expenses(email, email_param):
        user = User.query.filter_by(email=email_param).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        expenses = Expense.query.filter_by(user_id=user.id).all()
        expense_list = []
        for expense in expenses:
            expense_data = {
                'description': expense.description,
                'amount': expense.amount,
                'split_method': expense.split_method,
                'split_details': json.loads(expense.split_details) if expense.split_details else None
            }
            expense_list.append(expense_data)
        
        user_data = {
            'email': user.email,
            'name': user.name,
            'mobile_number': user.mobile_number,
            'expenses': expense_list
        }
        
        return jsonify(user_data)

    @app.route('/expenses/balance_sheet', methods=['GET'])
    @token_required
    def get_balance_sheet(email):
        users = User.query.all()
        overall_expenses = {}
        for user in users:
            user_expenses = Expense.query.filter_by(user_id=user.id).all()
            for expense in user_expenses:
                split_details = json.loads(expense.split_details) if expense.split_details else {}
                for participant_email, amount in split_details.items():
                    if participant_email in overall_expenses:
                        overall_expenses[participant_email] += amount
                    else:
                        overall_expenses[participant_email] = amount
        
        balance_sheet = []
        for email, amount in overall_expenses.items():
            user = User.query.filter_by(email=email).first()
            balance_sheet.append({
                'email': email,
                'name': user.name,
                'mobile_number': user.mobile_number,
                'total_expense': amount
            })

        return jsonify(balance_sheet)

    @app.route('/expenses/balance_sheet/download', methods=['GET'])
    # @token_required
    def download_balance_sheet(email):
        balance_sheet = get_balance_sheet(email).get_json()
        csv_data = "Email,Name,Mobile Number,Total Expense\n"
        for record in balance_sheet:
            csv_data += f"{record['email']},{record['name']},{record['mobile_number']},{record['total_expense']}\n"
        
        with open('balance_sheet.csv', 'w') as file:
            file.write(csv_data)

        return jsonify({'message': 'Balance sheet downloaded successfully'}), 200
