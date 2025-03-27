from django.shortcuts import render,redirect

from django.contrib.auth import login, logout, update_session_auth_hash
from django.views.generic import FormView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, ProfileForm
from django.urls import reverse_lazy
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm


# მომხმარებლის გამოსვლის კლასი
class LogoutUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('cars:index')

# მომხმარებლის შესვლის კლასი
class LoginUserView(LoginView):
    template_name = 'users/login.html'


class RegistrationUserView(FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('cars:index')

    def form_valid(self, form):
        user = form.save() #იქმნება ახალი იუზერი RegistrationForm ის გავლით User ის მეშვეობით
        login(self.request, user) # ჯანგოს login ის ფუნქციით იღებს მოთხოვნას და ახლადშექმნილ იუსერს და იწყება სესია
        return super().form_valid(form) #FormView კლასის ფუნქციის გამოძახება ხდება form_valid და საბოლოდ საწყის გვერდს უბრუნდება

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    #მეთოდი self.get_context_data(form=form) ამატებს ფორმას ვალიდაციის შეცდომით პახუის კონტექსტში, რათა ფორმა ხელახლა გამოისახოს შაბლონში და მომხმარებელმა შეძლოს მათი გამოსწორება.


#ეს კლასი პასუხისმგებელია მომხმარებლის პროფილის ჩვენებაზე და პირადი ინფორმაციისა და პაროლის შეცვლის ფორმის ჩვენებაზე.
#ხოლო თუ პოსტ მომართვაა ამ შემთხვევაში პროფილის ან პაროლის განახლების მოთხოვნის დამუშავებას ახორციელებს

class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile) #ProfileForm არის ჯანგოს ფორმა რომელიც იყენებს Profile მოდელს ფორმის გენერაციისთვის.
        password_form = PasswordChangeForm(user=request.user) #პაროლის შეცვლის ფორმა

        context = {
            'profile': profile,
            'profile_form': profile_form,
            'password_form': password_form

        }

        return render(request, 'users/profile.html', context)
    #ინფორმაციის განახლების ფუნქცია
    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile) #ხდება პოსტ მეთოდის ინციალიზაცია, და ნებისმიერი გადაცემული ფაილის მა.გამოსახულების

        password_form = PasswordChangeForm(user=request.user, data=request.POST) #პოსტ მეთოდით პაროლის შეცვლის ფორმა

        if 'update_profile' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('users:profile')

        if 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  #update_session_auth_hash ამ ფუნქციით ჰაში ახლდებადა მომხმარებელი რჩება ავტორიზირებული.
                return redirect('users:profile')

        context = {
            'profile_form': profile_form,
            'password_form':password_form

        }
        #კონტექსტი ნახლდება შესაბამისი ფორმებით და გამოიყენება შაბლონის რენდერისთვის

        return render(request, 'users/profile.html', context) #თუ ფორმამ ვალიდაცია ვერ გაიარა მოხდება შეცდომების რენდერი.


