from numpy import inner
from covid19.forms import CovidUpdateForm
from .models import CovidUpdate
from django.shortcuts import render
from django.contrib import messages
import pandas as pd 

# Create your views here.
def home(request):
    update = {}
    message = ""
    if request.method=='POST':   
        form = CovidUpdateForm(request.POST)     
        if form.is_valid():
            try:
                search = request.POST.get('search') 
                state_code_data = pd.read_csv('state_code.csv')
                state_code = state_code_data.loc[state_code_data['State'] ==search, "State_code"].iloc[0]
                url = "https://www.covid19india.org/state/"+state_code

                update['search'] = search
                update['code'] = state_code
                update['url'] = url
                update['scd'] = state_code_data


                daily_update = pd.read_csv("state_wise_daily.csv")
                confirmed = daily_update.loc[daily_update['Status']=='Confirmed', ['Date',state_code]]
                confirmed.rename(columns = {state_code: "Confirmed"},inplace=True)               
                recovered = daily_update.loc[daily_update['Status']=='Recovered',['Date', state_code]]
                recovered.rename(columns={state_code:"Recovered"}, inplace=True)
                decease = daily_update.loc[daily_update['Status']=='Deceased',['Date', state_code]]
                decease.rename(columns={state_code:"Deceased"}, inplace=True)
                update['confirmed'] = confirmed
                update['recovered'] = recovered
                update['decease'] = decease

                temp = pd.merge(confirmed,recovered, on='Date', how=inner)
                final_state_wise = pd.merge(temp, decease, on='Date', how=inner)
                final_state_wise['Active'] = final_state_wise['Confirmed'] - final_state_wise['Recovered'] - final_state_wise['Deceased']
                active = final_state_wise['Active']
                update['active'] = active

                final_state_wise['cf_Confirmed'] = final_state_wise['Confirmed'].cumsum()
                final_state_wise['cf_Recovered'] = final_state_wise['Recovered'].cumsum()
                final_state_wise['cf_Deceased'] = final_state_wise['Deceased'].cumsum()
                final_state_wise['cf_Active'] = final_state_wise['Active'].cumsum()
                cf_confirm = final_state_wise['cf_Confirmed']
                cf_recovered = final_state_wise['cf_Recovered']
                cf_deceased = final_state_wise['cf_Deceased'] 
                cf_active = final_state_wise['cf_Active']
                update['cf_confirm'] = cf_confirm
                update['cf_recovered'] = cf_recovered
                update['cf_deceased'] = cf_deceased
                update['cf_active'] = cf_active

                final_state_wise = final_state_wise[['Date','cf_Confirmed','cf_Recovered','cf_Deceased','cf_Active']]
                total_state_data = final_state_wise.tail(1)
                final_state_wise.Date = pd.to_datetime(final_state_wise.Date)

                update['final_state_wise'] = final_state_wise
                update['totaltotal_state_data'] =total_state_data
                update['final_state_wise_date'] = final_state_wise.Date
                
                print(final_state_wise.Date)

            except:
                # update['message ']= "Please Enter Correct State Name..........."
                # message = "Please Enter Correct State Name..........."
                pass
    
    form = CovidUpdateForm()
    context = {
        'form':form,
        'update':update,
        'errorcode':message,
        
    }
    print(update)
    return render(request, 'covid19/home.html',context) 




# def search(request):
    
#     if request.method=='POST':        
#         search = request.POST.get('search')
#         print(search)
#     context = {  }
#     return render(request, 'covid19/home.html',context)