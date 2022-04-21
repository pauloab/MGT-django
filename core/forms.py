from django.forms import ModelForm, EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from datetimewidget.widgets import DateTimeWidget

from core.models import Tarea


class TareaForm(ModelForm):

    class Meta:
        model = Tarea
        fields = ['nombre', 'tipo', 'fecha_tarea', 'valor_acordado','cancelado' , 'notas_adicionales']
        widgets = {
            #Use localization and bootstrap 3
            'fecha_tarea': DateTimeWidget(attrs={'id':"fecha_tarea"}, usel10n = True, bootstrap_version=3)
        }

class NewUserForm(UserCreationForm):
	email = EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user