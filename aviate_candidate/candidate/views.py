from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from candidate.models import Candidate
from candidate.serializers import CandidateSerializer

import traceback
import logging

logger = logging.getLogger("__name__")

class CandidateViewSet(viewsets.ModelViewSet):
    """
    Using modelviewset to create needed apis to create, update, delete using out of the box solution.
    Not using mixins as modelviewse will cover them all and search will be a different end point as it needs custom code.
    Overriding list method to accomodate relevancy based search.
    Skipping permission, authentication/authorisation for the test.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [] #allowany for test

class CandidateSearchView(APIView):
    """
    Using a separate custom end point for search.
    Not using drf search option to fit our custom relevancy based ordering

    """
    def post(self, request):
        try:
            search_text = request.data.get("name", None)
            if not search_text:
                logger.error(f'No valid search name provided.')
                return Response({'response': 'No valid search name provided.'}, status=status.HTTP_400_BAD_REQUEST)
            candidates = Candidate.objects.filter(name__icontains=search_text.lower()).values('name')
            #--------
            #logic for relevacy based ordering -
            #Assuming name shall at most have three words (first name, middle name and last name),
            #two words (first name and last name)
            #one word - only first name
            #--------
            #examples provided :[“Ajay Kumar Yadav”, “Ajay Kumar”, “Ajay Yadav”, “Kumar Yadav”, “Ramesh Yadav”, “Ajay Singh”]
            #Could not find first name, middle name, last name based weightage from examples  provided above, that works
            #For cases where in two words are matched (“Ajay Kumar”, “Ajay Yadav”, “Kumar Yadav) and only one word is matched (“Ramesh Yadav”, “Ajay Singh”).
            #Also alphabetical order is not consistent between two words match and one word match
            #--------
            #Assuming different ordering for three word match, two word match and one word match
            #Will do alphabetical ordering in case of three word match and two work match and
            #in case of one word match - weightage/order is last_name, first_name and then middle name
            #exact match shall be the first result
            #---
            #Not handling use cases where in there could be multiple users with same name, will have to find a way to order them, may be using one other value
            #There are lot more use cases depending on the design/plan, and will need more examples and expected behavior to handle them
            #For test purpose only returning name of the candidate and not the entire candidate info
            search_text_split = search_text.strip().split(" ")
            if len(search_text_split) > 3:
                return Response({'response': 'Name cannot be more than three words'}, status=status.HTTP_400_BAD_REQUEST)
            f_name = search_text_split[0]
            m_name = ""
            l_name = ""
            if len(search_text_split) == 3:
                m_name = search_text_split[1]
                l_name = search_text_split[2]
            if len(search_text_split) == 2:
                l_name = search_text_split[1]
            logger.info(f"len(search_text_split) : {len(search_text_split)}")
            logger.info(f"f_name, m_name, l_name:  {f_name} - {m_name} - {l_name}")
            search_results = []
            #case 1 :three word name search e.g. search for  ajay kumar yadav
            if f_name and m_name and l_name:
                q_three_words_match = Candidate.objects.filter(
                    Q(name__icontains=f_name) & Q(name__icontains=m_name) & Q(name__icontains=l_name)).order_by('name').values_list('name', flat=True)
                #With time may be can optimise the db query below, may be get cound of matches somehow,  but the high level idea  is the same.
                q_two_words_match = Candidate.objects.filter(
                    (Q(name__icontains=f_name) & Q(name__icontains=m_name) & ~Q(name__icontains=l_name)) |
                    (Q(name__icontains=f_name) & Q(name__icontains=l_name) & ~Q(name__icontains=m_name)) |
                    (Q(name__icontains=m_name) & Q(name__icontains=l_name) & ~Q(name__icontains=f_name))
                    ).order_by('name').values_list('name', flat=True)
                #order/priority for one word match - last_name, first_name and  then middle name
                #Separate calls for reach match so that first name matches can be handled first, with ordering and then last name ..and then middle name
                q_one_word_match_l = Candidate.objects.filter(
                    (Q(name__icontains=l_name) & ~Q(name__icontains=f_name) & ~Q(name__icontains=m_name))).order_by('name').values_list(
                    'name', flat=True)
                q_one_word_match_f = Candidate.objects.filter((Q(name__icontains=f_name) & ~Q(name__icontains=m_name) & ~Q(name__icontains=l_name))).order_by('name').values_list(
                    'name', flat=True)
                q_one_word_match_m = Candidate.objects.filter((Q(name__icontains=m_name) & ~Q(name__icontains=l_name) & ~Q(name__icontains=f_name))).order_by('name').values_list(
                    'name', flat=True)
                q_one_word_match = list(q_one_word_match_l) + list(q_one_word_match_f) + list(q_one_word_match_m)
                search_results = list(q_three_words_match) + list(q_two_words_match) + list(q_one_word_match)
            #case 2: two word name search -e.g. search for ajay kumar
            elif f_name and l_name and not m_name:
                q_two_words_match = Candidate.objects.filter(Q(name__icontains=f_name) & Q(name__icontains=l_name)).order_by('name').values_list('name', flat=True)
                q_one_word_match_l = Candidate.objects.filter((Q(name__icontains=l_name) & ~Q(name__icontains=f_name))).order_by('name').values_list('name', flat=True)
                q_one_word_match_f = Candidate.objects.filter((Q(name__icontains=f_name) & ~Q(name__icontains=l_name))).order_by('name').values_list('name', flat=True)
                q_one_word_match = list(q_one_word_match_l) + list(q_one_word_match_f)
                search_results = list(q_two_words_match) + list(q_one_word_match)
            #case three one word name search e.g. search for ajay
            elif f_name and not l_name and not m_name:
                q_one_word_match = Candidate.objects.filter((Q(name__icontains=f_name))).order_by('name')
                search_results = q_one_word_match.values_list('name', flat=True)
            #exact match
            try:
                exact_match = Candidate.objects.get(name__iexact=search_text.strip())
            except Candidate.DoesNotExist:
                exact_match = None
            logger.info(f"exact_match : {exact_match}")
            if exact_match:
                exact_match = exact_match.name
                search_results.remove(exact_match)
                search_results.insert(0, exact_match)
            return Response({'candidates':search_results}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'error while extracting segment text {traceback.format_exc()}')
            return Response({'response': 'Error while searching for candidate'}, status=status.HTTP_400_BAD_REQUEST)

    
