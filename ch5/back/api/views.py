from django.http.response import JsonResponse
from rest_framework.decorators import api_view
import joblib
import numpy as np
from .fis import FIS


@api_view(['POST'])
def result(request):
    if request.method == 'POST':

        dic = {}
        gest = int(request.data['gest'])
        birthweight = float(request.data['birthweight'])
        MAS = request.data['MAS']

        print(['level 3'], request.data['level_3'])

        if MAS == True:
            MAS = 1
        else:
            MAS = 0

        gender = request.data['gender']
        if gender == 'male':
            gender = 0
        else:
            gender = 1

        Multip = request.data['multip']
        if Multip == True:
            Multip = 1
        else:
            Multip = 0

        Level3 = request.data['level_3']
        if Level3 == True:
            Level3 = 1
        else:
            Level3 = 0
            print('level 3 false')

        dic['gest'] = gest
        dic['birthweight'] = birthweight
        dic['MAS'] = MAS
        dic['gender'] = gender
        dic['Multip'] = Multip
        dic['Level3'] = Level3


        # Load model
        male = joblib.load('./models/male.pkl')
        female = joblib.load('./models/female.pkl')
        FUZZY = FIS()

        array = list(dic.values())
        array = np.array(array).reshape(1, 6)



        # ges, weight, gender, mas, multip, level3
        ges_fuuzy = array[0][0]
        weight_fuzzy = array[0][1]
        gender_fuzzy = array[0][3]
        mas_fuzzy = array[0][2]
        multip_fuzzy = array[0][4]
        level3_fuzzy = array[0][5]

        fuzzyPro = FUZZY.input(
            ges_fuuzy, weight_fuzzy, gender_fuzzy, mas_fuzzy, multip_fuzzy, level3_fuzzy)


        if gender == 0:
            male_pre = male.predict_proba(array)
            male_val = round((male_pre[0][0]*100), 1)

            if array[0][2] == 0:
                array[0][2] = 1

                male2 = male.predict_proba(array)

                if male2[0][0] - male_pre[0][0] > 0.3:
                    steroid = 'Steroid given to mother is suggested'
                    return JsonResponse({'steroid': steroid, 'treePro': male_val, 'fuzzyPro': fuzzyPro})
                else:
                    steroid = 'Steroid is not important for mother'
                    return JsonResponse({'steroid': steroid, 'treePro': male_val, 'fuzzyPro': fuzzyPro})
            else:
                array[0][2] = 0
                male2 = male.predict_proba(array)

                if male_pre[0][0] - male2[0][0] > 0.3:
                    steroid = 'Steroid given to mother is suggested'

                    return JsonResponse({'steroid': steroid, 'treePro': male_val, 'fuzzyPro': fuzzyPro})
                else:
                    steroid = 'Steroid is not important for mother'

                    return JsonResponse({'steroid': steroid, 'treePro': male_val, 'fuzzyPro': fuzzyPro})

        else:  # female
            female_pre = female.predict_proba(array)
            female_val = round(female_pre[0][0]*100, 1)

            if array[0][2] == 0:
                array[0][2] = 1
                # [[0.96363636 0.03636364]] [[0.99393939 0.00606061]]
                female2 = female.predict_proba(array)

                if female2[0][0] - female_pre[0][0] > 0.3:
                    steroid = 'Steroid given to mother is suggested'
                    return JsonResponse({'steroid': steroid, 'treePro': female_val, 'fuzzyPro': fuzzyPro})

                else:
                    steroid = 'Steroid is not important for mother'
                    return JsonResponse({'steroid': steroid, 'treePro': female_val, 'fuzzyPro': fuzzyPro})

            else:
                array[0][2] = 0
                female2 = female.predict_proba(array)

                if female_pre[0][0] - female2[0][0] > 0.3:
                    steroid = 'Steroid given to mother is suggested'
                    return JsonResponse({'steroid': steroid, 'treePro': female_val, 'fuzzyPro': fuzzyPro})

                else:
                    steroid = 'Steroid is not important for mother'
                    return JsonResponse({'steroid': steroid, 'treePro': female_val, 'fuzzyPro': fuzzyPro})
