from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rango.models import Bares, Tapas
from rango.forms import BaresForm, TapasForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def index(request):
    
    bares_list = Bares.objects.order_by('-likes')[:5]
    tapas_list = Tapas.objects.order_by('-views')[:5]

    context_dict = {'baress': bares_list, 'tapas': tapas_list}

    return render(request, 'rango/index.html', context_dict)


def bares(request, bares_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        
        bares = Bares.objects.get(slug=bares_name_slug)
        context_dict['bares_name'] = bares.name

        tapas = Tapas.objects.filter(bares=bares)

        context_dict['tapas'] = tapas
        context_dict['bares'] = bares

	bares.views += 1
	bares.save()

    except Bares.DoesNotExist:
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/bares.html', context_dict)


def add_bares(request):
    if request.method == 'POST':
        form = BaresForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new bares to the database.
            form.save(commit=True)

            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = BaresForm()

    return render(request, 'rango/add_bares.html', {'form': form})


def add_tapas(request, bares_name_slug):

    try:
        bar = Bares.objects.get(slug=bares_name_slug)
    except Bares.DoesNotExist:
        bar = None

    if request.method == 'POST':
        form = TapasForm(request.POST)
        if form.is_valid():
            if bar:
                tapas = form.save(commit=False)
                tapas.bares = bar
                tapas.views = 0
                tapas.save()
                # probably better to use a redirect here.
                return bares(request, bares_name_slug)
        else:
            print form.errors
    else:
        form = TapasForm()

    context_dict = {'form':form, 'bares':bar}

    return render(request, 'rango/add_tapas.html', context_dict)


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance.
            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'rango/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered} )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:

                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')

@login_required
def like_bares(request):

    bar_id = None
    if request.method == 'GET':
        bar_id = request.GET['bares_id']

    likes = 0
    if bar_id:
        bar = Bares.objects.get(id=int(bar_id))
        if bar:
            likes = bar.likes + 1
            bar.likes =  likes
            bar.save()

    return HttpResponse(likes)



def reclama_datos (request):

	bares = Bares.objects.all()
	datos = []

	for bar in bares:
		datos.append({'name': bar.name, 'data':[bar.views]})



	return JsonResponse(datos, safe=False)


def about(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "Rango says here is the about page."}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'rango/about.html', context_dict)

