from django import forms

from combat.models import STRIKES
from hero.models import Hero

from django.forms.extras.widgets import SelectDateWidget

import datetime

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
        raise forms.ValidationError('Max level must be large than min level.')
    
    def clean_two_team_lvl_max(self):
        if 'two_team_lvl_min' in self.cleaned_data:
            two_team_lvl_max = self.cleaned_data['two_team_lvl_max']
            two_team_lvl_min = self.cleaned_data['two_team_lvl_min']
            if two_team_lvl_max >= two_team_lvl_min:
                return two_team_lvl_max
#
        raise forms.ValidationError('Max level must be large than min level.')
    
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
        raise forms.ValidationError('Max level must be large than min level.')
    
class PastForm(forms.Form):
#
    login = forms.CharField(max_length=32, label='Login')
##
    date_begin = forms.DateField(initial=datetime.date.today,
                            widget=SelectDateWidget(years=range(2000, 2012)), 
                                 label='Start date')
    date_end = forms.DateField(initial=datetime.date.today,
                            widget=SelectDateWidget(years=range(2000, 2012)), 
                               label='End date')
    
    def clean_date_end(self):
        date_begin = self.cleaned_data['date_begin']
        date_end = self.cleaned_data['date_end']   
        if date_begin > date_end:
#
            raise forms.ValidationError('Date begin must be smaller or same ' 
                                        'than date end.')
        return date_end
    
    def clean_login(self):
        login = self.cleaned_data['login']
        try:
            Hero.objects.get(login=login)
        except Hero.DoesNotExist:
#
            raise forms.ValidationError('Login does not exists.')
        
        return login
    
class CombatForm(forms.Form):
    def __init__(self, strike_count, block_count, hero_two_id, *args, 
                 **kwargs):
        self.strike_count = int(strike_count)
        self.block_count = int(block_count)  
        self.hero_two_id = hero_two_id
        super(CombatForm, self).__init__(*args, **kwargs)
        for strike in range(self.strike_count):
            self.fields['strike'+str(strike)] = forms.IntegerField(widget=
                                        forms.RadioSelect(choices=STRIKES),
                                                                required=False)
        self.fields['hero_two_id'] = forms.IntegerField(widget=
                        forms.HiddenInput(attrs={'value' : self.hero_two_id}))
        
        
    block_head = forms.BooleanField(label='Head', required=False)
    block_breast = forms.BooleanField(label='Breast', required=False)
    block_zone = forms.BooleanField(label='Zone', required=False)
    block_legs = forms.BooleanField(label='Legs', required=False)
        
    def clean(self):
        cleaned_data = self.cleaned_data
        
        if 'next' in self.data:
            cleaned_data['next'] = True
            return cleaned_data
        cleaned_data['next'] = False
        
        for strike in range(self.strike_count):
            if 'strike'+str(strike) not in cleaned_data:
#
                self._errors['strike0'] = self.error_class(
                                                ['This field is required.'])
                break
                
        k = 0
        block_head = cleaned_data.get('block_head')
        block_breast = cleaned_data.get('block_breast')
        block_zone = cleaned_data.get('block_zone')
        block_legs = cleaned_data.get('block_legs')
        if block_head: k += 1
        if block_breast: k += 1
        if block_zone: k += 1
        if block_legs: k += 1
        
        if self.block_count < k:
#
            self._errors['block_head'] = self.error_class(
                                                    ['This field is wrong.'])
        elif self.block_count > k:
#
            self._errors['block_head'] = self.error_class(
                                                ['This field is required.'])        
        
        return cleaned_data