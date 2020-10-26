from .forms import CreateProjectForm, CreateBidForm
from . models import Project, Bid, categories, Order, CompletedOrder
from django.shortcuts import HttpResponseRedirect, render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import Profile, UserPhone


@login_required
def orders(request):
    if CompletedOrder.objects.filter(user=request.user).exists():
        completedorders = CompletedOrder.objects.filter(user=request.user)
    else:
        completedorders = "no"
    if Order.objects.filter(worker=request.user).exists():
        orders = Order.objects.filter(worker=request.user)
    else:
        orders = "no"
    return render(request, 'projects/orders.html', {"orders": orders, "completed": completedorders})


@login_required
def category(request):
    category = categories.objects.all()
    return render(request, "projects/categories.html", {"categories": category})


@login_required
def Slug_Project(request, slug):
    projects = get_object_or_404(Project, slug=slug)
    if Bid.objects.filter(project=projects, created_by=request.user).exists():
        bids = Bid.objects.filter(project=projects, created_by=request.user)
        return render(request, "projects/project_detail.html", {"project": get_object_or_404(Project, slug=slug), "applied": bids})
    else:
        return render(request, "projects/project_detail.html", {"project": get_object_or_404(Project, slug=slug)})


@login_required
def Category_Project(request, category):
    user = request.user
    cat = get_object_or_404(categories, name=category)
    messages = Project.objects.filter(category=cat.id, completed=False)
    return render(request, "projects/cat_projects.html", {"user": user, "projects": messages, "category": cat})


@login_required
def CreateProject(request):
    profile = Profile.objects.get(user__id=request.user.id)
    user = request.user
    if request.method == 'POST':
        print('yes')
        form = CreateProjectForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                obj = Project(name=form.cleaned_data['name'], budget=form.cleaned_data['budget'], created_by=user, end_date=form.cleaned_data['end_date'], category=form.cleaned_data['category'], description=form.cleaned_data['description'], file=request.FILES['file'])
            else:
                obj = Project(name=form.cleaned_data['name'], budget=form.cleaned_data['budget'], created_by=user, end_date=form.cleaned_data['end_date'], category=form.cleaned_data['category'], description=form.cleaned_data['description'])
            obj.save()
        return HttpResponseRedirect("/projects/")
    else:
        if profile.completed is True and UserPhone.objects.filter(user=request.user).exists():
            form = CreateProjectForm()
            category = categories.objects.all()
            return render(request, "projects/project_new.html", {'user': user, 'categories': category}) 
        else:
            return redirect('/editprofile')


@login_required
def Projects(request):
    messages = Project.objects.filter(completed=False)
    return render(request, "projects/projects.html", {'projects': messages})


@login_required
def BidProject(request, project):
    user = request.user
    if request.method == 'POST':
        form = CreateBidForm(request.POST)
        if form.is_valid():
            obj = Bid(project=get_object_or_404(Project, slug=project), budget=form.cleaned_data['budget'], created_by=user, date_time=form.cleaned_data['date_time'], description=form.cleaned_data['description'])
            obj.save()
            return redirect("/projects/")
        return redirect("/projects/")
    else:
        profile = Profile.objects.get(user__id=request.user.id)
        if UserPhone.objects.filter(user=request.user).exists() and profile.completed is True:
            form = CreateBidForm()
            return render(request, "projects/bid.html", {'user': user, 'project': get_object_or_404(Project, slug=project)}) 
        return redirect("/editprofile")


@login_required
def Myprojects(request):
    projects = Project.objects.filter(created_by=request.user)
    return render(request, "projects/myprojects.html", {'projects': projects})


@login_required
def Applicants(request, project):
    projects = get_object_or_404(Project, slug=project)
    if request.user == projects.created_by:
        bids = Bid.objects.filter(project=projects)
        return render(request, "projects/applicant_bids.html", {'bids': bids, 'projects': projects})
    else:
        return redirect("dashboard:dashboard")

