import django.forms as forms
from .models import OrchidInstance, OrchidGenre, OrchidVariety, LIGHT_CHOICES, GROUND, MEDIUM, POT_TYPE, BLOOM

class AddOrchidInstanceForm(forms.ModelForm):
    class Meta:
        model = OrchidInstance
        exclude = ['user']

class AddOrchidGenreForm(forms.ModelForm):
    class Meta:
        model = OrchidGenre
        fields = "__all__"
        

class AddVarietyForm(forms.ModelForm):
    class Meta:
        model = OrchidVariety
        fields = "__all__"
    
    def clean_description(self):
        if not self.data["description"]:
            return OrchidGenre.objects.get(genre=self.data["genre"]).description
        return self.data["description"]
    
    def clean_winter_range(self):
        if not self.data["winter_range"]:
            return OrchidGenre.objects.get(genre=self.data["genre"]).winter_range
        return self.data["winter_range"]
    
    def clean_summer_range(self):
        if not self.data["summer_range"]:
            return OrchidGenre.objects.get(genre=self.data["genre"]).summer_range
        return self.data["summer_range"]
    
    def clean_light(self):
        if not self.data["light"]:
            return OrchidGenre.objects.get(genre=self.data["genre"]).light
        return self.data["light"]
    
    def clean_ground(self):
        if not self.data["ground"]:
            return OrchidGenre.objects.get(genre=self.data["genre"]).ground
        return self.data["ground"]
    
    def clean_humidity(self):
        if not self.data["humidity"]:
            return OrchidGenre.objects.get(genre=self.data["genre"]).humidity
        return self.data["humidity"]
    
    def clean_bloom(self):
        if not self.data["bloom"]:
            return OrchidGenre.objects.get(genre=self.data["genre"]).bloom
        return self.data["bloom"]


COMPARISONS = (
    ('lt', '<'),
    ('lte', '<='),
    ('exact', '=='),
    ('gte', '>='),
    ('gt', '>'),
)

class FilteredSearchForm(forms.Form):
    genre = forms.ModelChoiceField(OrchidGenre.objects.all(), required=False)
    mines = forms.BooleanField(required=False)
    light = forms.MultipleChoiceField(choices=LIGHT_CHOICES, required=False)
    humidity = forms.IntegerField(required=False, min_value=0, max_value=100)
    humidity_compare = forms.ChoiceField(choices=COMPARISONS, required=False, initial="exact")
    ground = forms.MultipleChoiceField(choices=GROUND, required=False)
    bloom = forms.MultipleChoiceField(choices=BLOOM, required=False)