from django import forms

from django.forms.extras.widgets import SelectDateWidget

class DuelForm(forms.Form):
    with_things = forms.BooleanField(required=False)
    TIME_OUTS = ((60, 60), (120, 120), (180,180))
    time_out = forms.IntegerField(widget=forms.Select(choices=TIME_OUTS))
    INJURIES = ((0, 'Low'), (1, 'Middle'), (2, 'Top'))
    injury = forms.IntegerField(widget=forms.Select(choices=INJURIES))
    
class GroupForm(forms.Form):
    with_things = forms.BooleanField(required=False)
    TIME_OUTS = ((60, 60), (120, 120), (180,180))
    time_out = forms.IntegerField(widget=forms.Select(choices=TIME_OUTS))
    INJURIES = ((0, 'Low'), (1, 'Middle'), (2, 'Top'))
    injury = forms.IntegerField(widget=forms.Select(choices=INJURIES))
    TIME_WAITS = ((360, '5 min.'), (720, '10 min.'), (1440, '20 min.'))
    time_wait = forms.IntegerField(widget=forms.Select(choices=TIME_WAITS))
#
    one_team_count = forms.IntegerField(min_value=1, max_value=99, 
                                        label='First team', 
                                        widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
#
    two_team_count = forms.IntegerField(min_value=1, max_value=99,
                                        label='Second team',
                                        widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
    one_team_lvl_min = forms.IntegerField(min_value=0, max_value=99,
                                          widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
    one_team_lvl_max = forms.IntegerField(min_value=0, max_value=99,
                                          widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
    two_team_lvl_min = forms.IntegerField(min_value=0, max_value=99,
                                          widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
    two_team_lvl_max = forms.IntegerField(min_value=0, max_value=99,
                                          widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
    
    def clean_one_team_lvl_max(self):
        if 'one_team_lvl_min' in self.cleaned_data:
            one_team_lvl_max = self.cleaned_data['one_team_lvl_max']
            one_team_lvl_min = self.cleaned_data['one_team_lvl_min']
            if one_team_lvl_max >= one_team_lvl_min:
                return one_team_lvl_max
#
        raise forms.ValidationError('Max level must be large than min level')
    
    def clean_two_team_lvl_max(self):
        if 'two_team_lvl_min' in self.cleaned_data:
            two_team_lvl_max = self.cleaned_data['two_team_lvl_max']
            two_team_lvl_min = self.cleaned_data['two_team_lvl_min']
            if two_team_lvl_max >= two_team_lvl_min:
                return two_team_lvl_max
#
        raise forms.ValidationError('Max level must be large than min level')
    
class ChaoticForm(forms.Form):
    with_things = forms.BooleanField(required=False)
    TIME_OUTS = ((60, 60), (120, 120), (180,180))
    time_out = forms.IntegerField(widget=forms.Select(choices=TIME_OUTS))
    INJURIES = ((0, 'Low'), (1, 'Middle'), (2, 'Top'))
    injury = forms.IntegerField(widget=forms.Select(choices=INJURIES))
    TIME_WAITS = ((360, '5 min.'), (720, '10 min.'), (1440, '20 min.'))
    time_wait = forms.IntegerField(widget=forms.Select(choices=TIME_WAITS))
#
    count = forms.IntegerField(min_value=1, max_value=99, label='Count', 
                               widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
    lvl_min = forms.IntegerField(min_value=0, max_value=99,
                                 widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
    lvl_max = forms.IntegerField(min_value=0, max_value=99,
                                 widget=forms.TextInput(
                                            attrs={'size':1, 'maxlength':2}))
    
    def clean_lvl_max(self):
        if 'lvl_min' in self.cleaned_data:
            lvl_max = self.cleaned_data['lvl_max']
            lvl_min = self.cleaned_data['lvl_min']
            if lvl_max >= lvl_min:
                return lvl_max
#
        raise forms.ValidationError('Max level must be large than min level')
    
class PastForm(forms.Form):
    login = forms.CharField(max_length=32)
    date_begin = forms.DateField(widget=SelectDateWidget())
    date_end = forms.DateField(widget=SelectDateWidget())