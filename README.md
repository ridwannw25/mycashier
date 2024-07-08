# My Cashier

My Cashier is a simple cashier application that allows users to record and calculate revenue from sold items. This application is built using the Django framework.

## Overview

My Cashier is designed to help users record sales transactions of products and automatically calculate total revenue. Users can add products, manage stock, and view detailed sales reports.

## Key Features

- **Product Management:** Add, edit, and delete products with price and stock information.
- **Sales Transactions:** Record sales transactions, decrease product stock, and calculate total revenue.
- **Sales Reports:** View daily, weekly, or monthly sales reports to analyze sales statistics.

## Installation

To run this application on your local development environment, follow these steps:

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/ridwannw25/mycashier.git
   cd mycashier
   ```

2. Install dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

3. Perform database migration:
   ```
   python manage.py migrate
   ```

4. Create a superuser to access the Django admin panel:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Open your web browser and go to `http://localhost:8000` to access the My Cashier application.

## Usage

1. Log in to the application using the superuser credentials created earlier.
2. Add new products by clicking the "Add Product" button and filling out the form with appropriate information.
3. To make a sales transaction, select a product from the list of available products, enter the quantity sold, and click the "Sell" button.
4. The application will decrease the stock of the sold product and automatically calculate the total revenue.
5. You can view sales reports by accessing the reports page.

## Contribution

Community contributions are always welcome. To contribute, please submit a pull request with a clear description of the changes you propose.


## Contact

For more information or questions, please contact the development team at ridwannurwahid35@gmail.com.

## Project Status

This project is actively under development.
