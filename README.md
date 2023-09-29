# Apple sales reports

Welcome,  

This program provides various options for performing calculations and obtaining data. Users can choose between monthly, weekly, and daily calculations, and access a range of specific metrics related to sales and performance. Overall, it is a versatile tool for analyzing and calculating various aspects of data and performance.

The "Apple sales" data is stored in Google Sheet, which is used as a database, and using Google's APIs for Gdrive and Google sheets, relevant data is extracted from it and presented to the user based on their choice of calculations. Please note that the data used in this project is entirely fictitious. These data reflect activities that take place during the month of September.

[Here is a live link to my project](https://apple-sales-report-6a3868d388e4.herokuapp.com/)


![Responsive design](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1695908616/apple-sales/responsive_cepgvv.jpg)

## Features

When you start the program, the welcome screen displays the program name and offers three options to choose from: start calculations, about the program, and end the program.

![menu](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1695909539/apple-sales/1_option_l1b0mj.jpg)

If the user selects "Start calculations", he is offered a choice of monthly, weekly or daily calculations. The user can also return to the main menu or end the program.

![menu](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1695909254/apple-sales/2_option_v764zm.jpg)

### Get monthly calculations  

![menu](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1695910493/apple-sales/month_feucbr.jpg)

By clicking "Get FULL REPORT", the user gets a full monthly calculation which includes all calculations available in the following options (such as total sales, monthly average check, etc.). The user is also presented with a full table of data.

![menu](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1695909923/apple-sales/full_report_mk0t4r.jpg)

Each of these calculations serves a specific purpose in analyzing business performance, sales, profitability, and customer behavior. They provide valuable insights that can inform decision-making and help businesses optimize their strategies.

<details open>
  <summary>Get total sales</summary>
  <div style="margin: 10px 40px;">  
    Purpose: This calculation provides the total sales revenue for a specific period (e.g., month, week, or day). It gives you an overview of the overall revenue generated during that time frame.
  </div>
</details>

<details>
    <summary>Get weekly average check</summary>  
        <div style="margin: 10px 40px;"> 
            Purpose: The weekly average check calculates the average amount of money spent per transaction in a given week. It helps in understanding customer spending patterns on a weekly basis.
        </div>
</details>

<details>
    <summary>Get maximum sales</summary>  
        <div style="margin: 10px 40px;"> 
            Purpose: This calculation identifies the highest sales figure within the chosen period. It helps in recognizing the peak performance and the highest revenue achieved.
        </div>
</details>

<details>
    <summary>Get minimum sales</summary>  
        <div style="margin: 10px 40px;"> 
            Purpose: Similar to maximum sales, this calculation identifies the lowest sales figure within the chosen period. It helps in identifying periods of low performance or potential issues.
        </div>
</details>

<details>
    <summary>Get profit</summary>  
        <div style="margin: 10px 40px;"> 
            Purpose: Profit calculation subtracts the costs or expenses from the total revenue. It provides insights into the profitability of your business for a specific time frame.
        </div>
</details>

<details>
    <summary>Get order average check</summary>  
        <div style="margin: 10px 40px;"> 
            Purpose: The order average check calculates the average amount spent by customers per order. It helps in understanding individual purchase behavior and can guide pricing strategies.
        </div>
</details>

<details>
    <summary>Get conversion rate</summary>  
        <div style="margin: 10px 40px;"> 
            Purpose: Conversion rate measures the percentage of customers who take a desired action, such as making a purchase or completing a form. It helps evaluate the effectiveness of marketing campaigns and website optimization.
        </div>
</details>

<details>
    <summary>Get ROI (Return on Investment)</summary>  
        <div style="margin: 10px 40px;"> 
            Purpose: ROI measures the return (profit) on an investment relative to the initial cost (investment). It is used to assess the performance and profitability of investments or marketing campaigns. A positive ROI indicates profitability.
        </div>
</details>

### Get weekly calculations
Once the user enters the number of the week they want to calculate, they will be presented with all the data with calculations for that particular week, as well as will be returned to the previous menu.

![menu](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1695911418/apple-sales/week_ol7zkr.jpg)
### Get daily data
After the user enters the number of the day (from 1 to 30), which he wants to calculate, he will be displayed all the data with calculations for a particular day, as well as return to the previous menu.

![menu](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1695912647/apple-sales/day_v2oc5g.jpg)

### Error messages

1. **Input Must Be a Number:**

Description: This error message is shown when the user enters non-numeric input.

![err](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1696002307/apple-sales/error_afaowm.jpg)  

2. **Input Out of Range:**  

Description: This error message is displayed when the user enters a numeric value that is outside the specified range.

![menu](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1696002360/apple-sales/error_t0afmr.jpg)
   

These error messages help guide users when they provide incorrect input and provide clear feedback on what went wrong.

## Future features

1. **Additional Data Sources:** Incorporate real data sources to make the calculations more realistic and practical.

2. **Custom Date Ranges:** Allow users to input custom date ranges for calculations, providing greater flexibility.

3. **Export Functionality:** Implement the ability to export calculation results to various file formats for further analysis.

4. **Enhanced Visualization:** Create interactive visualizations to help users better understand the data and metrics.

5. **Integration as a Library:** Transform this project into a reusable library for financial and sales calculations, making it accessible to a wider audience.

## Testing

I manually tested the project using the following methods:

- Testing the responsiveness of the deployed site on Heroku on various sizes of devices using Chrome tools.

- Testing browser compatibility with Firefox, Safari, and Chrome on the deployed site on Heroku.

- Tests for correctness of retrieving data about each calculation from a Google spreadsheet and displaying it in the program.

- Provided incorrect data to make sure appropriate error messages were issued.

- Tested the code through [Pep8](https://pep8ci.herokuapp.com/#) to make sure there are no critical issues.  

![pep8](https://res.cloudinary.com/dsmrhqdnv/image/upload/v1696002744/apple-sales/cli_sdaijb.jpg)

## Deployment 
In order to deploy the project on Heroku, the following steps were taken:

Activate Dyno points in the billing section of the Heroku account settings.

In the Heroku dashboard create a new project and give it a name.

In the project settings add 2 config vars (kEY: Creds VALUE: Copy and paste the credentials from the creds.json file and a second configuration KEY: PORT with VALUE: 8000).

Also in the project settings add two build packs (A python build pack and a node.js build pack in that order).

Then go to the deploy tab of the project and connect the project's Github repository.

After the Github repository has been connected, select the manual deploy option which will deploy the project if no errors arise.

## Credits

The background image was taken from [getwallpapers.com](https://getwallpapers.com/collection/nature-wallpapers-full-screen)