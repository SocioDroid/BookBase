from django.http import JsonResponse
from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from .models import Sell, UserProfileInfo, Notify, Sold
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from matplotlib import pyplot as plt
from django.conf import settings
import os
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SellForm
import urllib.request
import urllib.parse
from django.contrib.auth.models import User
from .models import UserProfileInfo
import pandas as pd
import numpy as np
import operator
@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            return HttpResponseRedirect('/user/login/')
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'signup.html',{
                                            'user_form':user_form,
                                            'profile_form':profile_form,
                                            'registered':registered
                                        })


def dashboard(request):

    if request.method == 'GET' and 'notID' in request.GET:
        nid = request.GET.get('notID')
        # retVal = ""
        one_task = Sell.objects.get(add_id=nid)
        if one_task:
            print('task =' ,one_task)

            one_task.delete()  # line 1
            #two_task = Sell.objects.get(id=nid)

            # print(retVal)
            return JsonResponse({
                'id':"Advertisement is deleted."
            })

    if request.method == 'GET' and 'notificationID' in request.GET:
        nid = request.GET.get('notificationID')
        # retVal = ""
        one_task = Notify.objects.get(notify_id=nid)
        if one_task:
            print('task =' ,one_task)

            one_task.delete()  # line 1
            #two_task = Sell.objects.get(id=nid)

            # print(retVal)
            return JsonResponse({
                'id':"Notifiaction is deleted."
            })
    if request.method == 'GET' and 'soldNID' in request.GET:
        nid = request.GET.get('soldNID')
        # retVal = ""
        one_task = Notify.objects.get(notify_id=nid)
        if one_task:
            sellRow = Sell.objects.get(add_id=one_task.add_id_id)

            soldModel = Sold()
            soldModel.title = sellRow.title
            soldModel.price = sellRow.price
            soldModel.save()

            sellRow.delete()
            # print(retVal)
            return JsonResponse({
                'id':"BOOK SOLD !"
            })

    notifications = Notify.objects.filter(seller_id_id=request.user.id)

    notificationList=[]

    for e in notifications:
        pair = {
            'notId': e.notify_id,
            'date': e.datetime,
            'buyer': User.objects.get(id=e.buyer_id_id),
            'prodName':Sell.objects.get(add_id = e.add_id_id)
        }
        notificationList.append(pair)

# ------------------------------------------------------- Advertisements List

    advt = Sell.objects.filter(user_id_id=request.user.id)
    advtList=[]

    for e in advt:
        pair = {
            'notId': e.add_id,
            'date': e.datetime,
            'author': e.author,
            'title':e.title

        }
        advtList.append(pair)

    context = {'pair':notificationList,'advt':advtList}

    return render(request, 'dash.html', context)


#OLD SELL
# def sell(request):
#     if request.method == 'GET':
#         title = request.GET.get('title')
#         #retVal = ""
#         if title:
#             retVal =  checkPrice(title)
#             #print(retVal)
#             return JsonResponse({
#                                  'avg': retVal[0],
#                                  'min': retVal[1],
#                                  'max': retVal[2],
#                                  'imagePath': retVal[3]
#                                  })
#         return render(request, 'sell.html', )
#
#     if request.method == 'POST'id_authorand request.FILES['myfile']:
#         title = request.POST.get('title')
#         author =request.POST.get('author')
#         description =request.POST.get('desc')
#         price =request.POST.get('price')
#         sellModel = Sell()
#         sellModel.title = title
#         sellModel.author = author
#         sellModel.description = description
#         sellModel.price = price
#         sellModel.user_id = request.user
#         sellModel.bookImage = request.FILES['myfile']
#         sellModel.save()
#         context = {'title':title,'author':author,'desc':description,'price':price}
#         print(str(title)+str(author)+str(description)+str(price))
#
#         return render(request,'sell.html', context)
#     else:
#         return render(request, 'sell.html', {})

#PRICE SUGGESTOR
def checkPrice(titleRec):
    bookPrice = []
    flag=False
    sum=0
    #Fetch the price for input title
    for e in Sell.objects.filter(title__icontains=titleRec):
        if e:
            bookPrice.append(e.price)
            flag=True
    if flag:
        bookPrice.sort()

        Sum = 0
        for e in bookPrice:
            Sum += e


        avg = Sum / len(bookPrice)
        avgPrice = 'Suggested Price : '+ str(avg)
        minPrice = 'Minimum Price : '+ str( bookPrice[0])
        maxPrice = 'Maximum Price : '+str(bookPrice[-1])
        # print(avgPrice)
        # print(minPrice)
        # print(maxPrice)
        #Make a list to return
        priceList = [avgPrice,minPrice,maxPrice]
        # Plot Graph
        plt.title(titleRec)
        # plt.text(0.5, 2.5, minPrice)
        # plt.text(0.5, 4.5, maxPrice)

        plt.scatter(range(len(bookPrice)),bookPrice)
        plt.savefig(os.path.join(settings.BASE_DIR,'static/user/images/'+titleRec+'.png'))
        figPath ="<img src="+'"'+"/static/user/images/"+titleRec+".png"+'"'+" height="+'"'+"50% width="+'"'+"50%"+'"'+">"

        priceList.append(figPath)
        print(figPath)
    return (priceList)

#SELL FORM
class CreatePostView(CreateView): # new
    model = Sell
    form_class = SellForm
    template_name = 'sell2.html'
    success_url = reverse_lazy('home')
    print("Inside Class")

    def form_valid(self, form):
        form.instance.user_id = self.request.user
       # print("Inside Def")
        super().form_valid(form)
        return HttpResponseRedirect('/user/dashboard')

    def get(self, request):
        title = request.GET.get('title')
        # retVal = ""
        if title:
            retVal = checkPrice(title)
            # print(retVal)
            return JsonResponse({
                'avg': retVal[0],
                'min': retVal[1],
                'max': retVal[2],
                'imagePath': retVal[3]
            })
        form =self.form_class(initial=self.initial)
        return render(request, 'sell2.html',{'form': form})

def BuyView(request):
    datalist= []
    if request.method == 'POST' and 'searchForm' in request.POST:
        booknm = request.POST.get('q')
        # gender = request.POST.get('list')
        # print(gender, "-----------------------------------------------")
        datalist = []
        for e in Sell.objects.filter(title__icontains=booknm):
            if e:
                context = {
                    'price':e.price,
                    'title':e.title,
                    'auth':e.author,
                    'descp':e.description,
                    'img':e.bookImage,
                    'add_id': e.add_id
                }
                datalist.append(context)
        return render(request, 'registration/buy.html', {'data':datalist})

    if request.method == 'POST' and 'sortForm' in request.POST:
        sortParam = request.POST.get('list')
        datalist = []
        if sortParam == "az":
            for e in Sell.objects.order_by('title'):
                if e:
                    context = {
                        'price':e.price,
                        'title':e.title,
                        'auth':e.author,
                        'descp':e.description,
                        'img':e.bookImage,
                        'add_id': e.add_id
                    }
                    datalist.append(context)
        elif sortParam == "za":
            for e in Sell.objects.order_by('-title'):
                if e:
                    context = {
                        'price':e.price,
                        'title':e.title,
                        'auth':e.author,
                        'descp':e.description,
                        'img':e.bookImage,
                        'add_id': e.add_id
                    }
                    datalist.append(context)
        elif sortParam == "aPrice":
            for e in Sell.objects.order_by('price'):
                if e:
                    context = {
                        'price':e.price,
                        'title':e.title,
                        'auth':e.author,
                        'descp':e.description,
                        'img':e.bookImage,
                        'add_id': e.add_id
                    }
                    datalist.append(context)
        elif sortParam == "dPrice":
            for e in Sell.objects.order_by('-price'):
                if e:
                    context = {
                        'price':e.price,
                        'title':e.title,
                        'auth':e.author,
                        'descp':e.description,
                        'img':e.bookImage,
                        'add_id': e.add_id
                    }
                    datalist.append(context)
        elif sortParam == "trending":
            # __________________________________________________trendingLogic
            res = Sold.objects.raw(
                "select sold_id,title, -CAST(julianday('now') - julianday(user_sold.datetime)AS INT) 'age', count(title) 'cnt' from user_sold GROUP BY title,age")

            soldList = []
            for i in res:
                l = []
                l.append(i.title)
                l.append(i.age)
                l.append(i.cnt)
                soldList.append(l)
            print("----------------------------")
            print(soldList)
            trending = calcTrending(soldList)
            # __________________________________________________trendingLogicEnds
            for i in trending:
                for e in Sell.objects.filter(title__icontains = i ):
                    if e:
                        context = {
                            'price': e.price,
                            'title': e.title,
                            'auth': e.author,
                            'descp': e.description,
                            'img': e.bookImage,
                            'add_id': e.add_id
                        }
                        datalist.append(context)

        return render(request, 'registration/buy.html', {'data':datalist})

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            buyerid = request.GET.get('user_id')
            prod_data = Sell.objects.get(add_id=id)
            buyer_data = User.objects.get(id=buyerid)
            buyer_data_phone = UserProfileInfo.objects.get(user_id=buyerid)
            seller_data = UserProfileInfo.objects.get(user_id=prod_data.user_id_id)

            print(buyer_data.username)

            #SENDING SMS--------------------------------------------------------------------------------------------------
            message = buyer_data.username + " is interested in buying " +prod_data.title+ " Contact Number :"+buyer_data_phone.phoneNo
            resp = sendSMS('Yn2kY8xfT5I-OD8YRS2lC8mXslywI4KqsphMz7WzWo', '91'+seller_data.phoneNo,'TXTLCL', message)
            print(resp)

            #ADDING DATA INTO NOTIFICATION TABLE
            notifyModel = Notify()
            notifyModel.add_id_id =prod_data.add_id
            notifyModel.seller_id_id=seller_data.user_id
            notifyModel.buyer_id_id=buyer_data.id
            notifyModel.save()

            if id:
                return JsonResponse({
                                     'id': prod_data.price
                                     })
            return render(request, 'buy.html', )
        else:

            #Default Sort A - Z
            for e in Sell.objects.order_by('title'):
                if e:
                    context = {
                        'price': e.price,
                        'title': e.title,
                        'auth': e.author,
                        'descp': e.description,
                        'img': e.bookImage,
                        'add_id':e.add_id
                    }
                    datalist.append(context)
            return render(request, 'registration/buy.html', {'data': datalist})

  #  return render(request, 'registration/buy.html', {})


def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return (fr)

def calcTrending(d):

    def train(data):
        df = pd.DataFrame(data, columns=['title', 'age', 'count'])
        df.sort_values(by=['title', 'age'], inplace=True)
        trends = pd.pivot_table(df, values='count', index=['title', 'age'])

        trend_snap = {}

        for i in np.unique(df['title']):
            trend = np.array(trends.loc[i])
            # smoothed = smooth(trend, SMOOTHING_WINDOW_SIZE, SMOOTHING_WINDOW_FUNCTION)
            nsmoothed = standardize(trend)
            slopes = nsmoothed[1:] - nsmoothed[:-1]
            # I blend in the previous slope as well, to stabalize things a bit and
            # give a boost to things that have been trending for more than 1 day
            if len(slopes) > 1:
                trend_snap[i] = slopes[-1] + slopes[-2] * 0.5
        return sorted(trend_snap.items(), key=operator.itemgetter(1), reverse=True)

    def standardize(series):
        iqr = np.percentile(series, 75) - np.percentile(series, 25)
        return (series - np.median(series)) / iqr

    trending = train(d)
    print("Top 5 trending products:")
    trendingList = []
    for i, s in trending[:5]:
        print("Product %s (score: %2.2f)" % (i, s))
        trendingList.append(i)
    return  trendingList

