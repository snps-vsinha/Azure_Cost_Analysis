from azure.identity import DefaultAzureCredential  
from azure.mgmt.costmanagement import CostManagementClient  
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod, QueryDataset, QueryAggregation  
from datetime import datetime  
import pandas as pd
import matplotlib.pyplot as plt
import os

budget=[3000]
subs_name=["SNPS-IPG-GenAI-SCS"]
subscription_id=["<+stage.variables.IPG>"]

for name, id, budget in zip(subs_name, subscription_id, budget):  
    '''Code for extracting the daily cost foar each of the subscription'''

    # Replace with your subscription ID  
    subscription_id = id
    subs= name 
    
    # Authenticate using DefaultAzureCredential  
    credential = DefaultAzureCredential()  
    
    # Initialize the CostManagementClient  
    cost_management_client = CostManagementClient(credential)  
    
    # Define the time period for the cost query  
    start_date = "2024-11-01T00:00:00Z"  
    end_date = "2024-11-21T23:59:59Z"  
    time_period = QueryTimePeriod(  
        from_property=start_date,  
        to=end_date  
    )  
    
    # Define the dataset with aggregation and grouping by day  
    dataset = QueryDataset(  
        aggregation={  
            "totalCost": QueryAggregation(  
                name="Cost",  
                function="Sum"  
            )  
        },  
        granularity="Daily"  
    )  
    
    # Define the query definition  
    query_definition = QueryDefinition(  
        type="Usage",  
        timeframe="Custom",  
        time_period=time_period,  
        dataset=dataset  
    )  
    cost=[] 
    # Execute the cost query  
    try:  
        query_result = cost_management_client.query.usage(  
            scope=f"/subscriptions/{subscription_id}",  
            parameters=query_definition  
        )  
    except Exception as e:  
        print(f"Error executing query: {e}")  
        raise  
    
    # Check the structure of the query result  
    if not query_result.rows:  
        print("No data returned for the specified period.")  
    else:  
        for row in query_result.rows:  
            cost.append(row[0]) 

    '''Code for generating the dataframe'''

    # Create the 'Date' range  
    dates = pd.date_range(start='2024-11-01', end='2024-11-30')  
    
    # Determine the length of the 'cost' list and the 'dates' range  
    num_days = len(dates)  
    num_cost_entries = len(cost)  
    
    # Extend the 'cost' list with 0s to match the length of the date range  
    cost.extend([0] * (num_days - num_cost_entries))  
    
    # Calculate 'Cumulative Daily Usage'  
    cumulative_daily_usage = pd.Series(cost).cumsum()  
    
    # Calculate 'Ideal Daily Usage'  
    ideal_daily_usage = budget / 30  
    
    # Calculate 'Ideal Cumulative Daily Usage'  
    ideal_cumulative_daily_usage = [ideal_daily_usage * (i + 1) for i in range(num_days)]  
    
    # Create the DataFrame  
    data = {  
        'Date': dates,  
        'Actual Daily Usage': cost,  
        'Cumulative Daily Usage': cumulative_daily_usage,  
        'Ideal Daily Usage': ideal_daily_usage,  
        'Ideal Cumulative Daily Usage': ideal_cumulative_daily_usage,  
        'Budgeted Cost for Subscription': budget  
    }  
    
    df = pd.DataFrame(data)  
 

    '''Code for generating and saving plots '''

    # Plotting the data  
    fig, ax1 = plt.subplots(figsize=(14, 7))  
    
    # Bar plots for 'Actual Daily Usage' and 'Ideal Daily Usage'  
    ax1.bar(df['Date'] - pd.Timedelta(days=0.2), df['Actual Daily Usage'], width=0.4, label='Actual Daily Usage')  
    ax1.bar(df['Date'] + pd.Timedelta(days=0.2), df['Ideal Daily Usage'], width=0.4, label='Ideal Daily Usage')  
    
    # Determine color for 'Cumulative Daily Usage'  
    cumulative_colors = ['red' if actual > ideal else 'green' for actual, ideal in zip(df['Cumulative Daily Usage'], df['Ideal Cumulative Daily Usage'])]  
    
    # Line plots for 'Cumulative Daily Usage', 'Ideal Cumulative Daily Usage', and 'Budgeted Cost for Subscription'  
    ax2 = ax1.twinx()  
    for i in range(len(df['Date']) - 1):  
        ax2.plot(df['Date'][i:i+2], df['Cumulative Daily Usage'][i:i+2], color=cumulative_colors[i])  
    
    ax2.plot(df['Date'], df['Ideal Cumulative Daily Usage'], label='Ideal Cumulative Daily Usage', color='black', linestyle=':')  
    ax2.axhline(y=budget, color='red', linestyle='-', linewidth=2, label='Budgeted Cost for Subscription')  
    
    # Labels and titles  
    ax1.set_xlabel('Date')  
    ax1.set_ylabel('Daily Usage')  
    ax2.set_ylabel('Cumulative Usage / Cost')  
    
    fig.suptitle(subs)  
    
    # Legends  
    ax1.legend(loc='upper left')  
    ax2.legend(loc='upper right')  
    
    # Formatting the x-axis to show all dates  
    ax1.set_xticks(df['Date'])  
    ax1.set_xticklabels(df['Date'].dt.strftime('%Y-%m-%d'), rotation=45)  
    
    plt.tight_layout()  
    # Save the plot with the name specified in subs_name  
    fig.savefig(os.path.join("./plots", f"{subs}.png"))
    # plt.show()

    print(subs,":done")
