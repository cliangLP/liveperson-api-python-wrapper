"""
Provides a Data Structure for a Conversation History Record from the Messaging Interactions API.
"""

from collections import namedtuple
from typing import List

# Declare new types to store each event from data.
Info = namedtuple('Info', ['conversation_id', 'brand_id', 'status', 'start_time', 'start_time_l', 'end_time',
                           'end_time_l', 'duration', 'close_reason', 'first_conversation', 'csat', 'csat_rate', 'mcs',
                           'alerted_mcs', 'source', 'device', 'latest_skill_id', 'latest_skill_name', 'latest_agent_id',
                           'latest_agent_login_name', 'latest_agent_nickname', 'latest_agent_full_name',
                           'latest_agent_group_id', 'latest_agent_group_name', 'browser', 'operating_system',
                           'latest_queue_state', 'is_partial'])

Campaign = namedtuple('Campaign', ['conversation_id', 'campaign_engagement_id', 'campaign_engagement_name',
                                   'campaign_id', 'campaign_name', 'goal_id', 'goal_name', 'engagement_agent_note',
                                   'engagement_source', 'visitor_behavior_id', 'visitor_behavior_name',
                                   'engagement_application_id', 'engagement_application_name',
                                   'engagement_application_type_id', 'engagement_application_type_name',
                                   'visitor_profile_id', 'visitor_profile_name', 'lob_id', 'lob_name', 'location_id',
                                   'location_name', 'behavior_system_default', 'profile_system_default'])

Message = namedtuple('MessageRecord', ['conversation_id', 'time', 'time_l', 'type', 'message_data', 'message_id', 'seq',
                                       'dialog_id', 'participant_id', 'source', 'device', 'sent_by', 'context_data'])

AgentParticipant = namedtuple('AgentParticipant', ['conversation_id', 'agent_id', 'agent_login_name', 'agent_nickname',
                                                   'agent_full_name', 'agent_deleted', 'time', 'time_l', 'role',
                                                   'user_type', 'user_type_name', 'agent_group_id', 'agent_group_name',
                                                   'permission'])

ConsumerParticipant = namedtuple('ConsumerParticipant', ['conversation_id', 'participant_id', 'time', 'time_l',
                                                         'first_name', 'last_name', 'phone', 'email', 'token'])

Transfer = namedtuple('Transfer', ['conversation_id', 'time', 'timeL', 'assignedAgentId', 'assignedAgentLoginName',
                                   'assignedAgentNickname', 'assignedAgentFullName', 'targetSkillId', 'targetSkillName',
                                   'sourceSkillId', 'sourceSkillName', 'sourceAgentId', 'sourceAgentLoginName',
                                   'sourceAgentNickname', 'sourceAgentFullName', 'reason', 'contextData'])

Interaction = namedtuple('Interaction', ['conversation_id', 'assigned_agent_id', 'agent_login_name', 'agent_nickname',
                                         'agent_full_name', 'interaction_time', 'interaction_time_l',
                                         'interactive_sequence'])

MessageScore = namedtuple('MessageScore', ['conversation_id', 'message_id', 'time', 'time_l', 'mcs',
                                           'message_raw_score'])

MessageStatus = namedtuple('MessageStatus', ['conversation_id', 'message_delivery_status', 'message_id',
                                             'participant_id', 'participant_type', 'seq', 'time', 'time_l'])

Survey = namedtuple('Survey', ['conversation_id', 'survey_type', 'survey_status', 'survey_question', 'survey_data'])

CoBrowseSession = namedtuple('CoBrowseSession', ['conversation_id', 'session_id', 'start_time', 'start_time_l',
                                                 'end_time', 'end_time_l', 'interactive_time', 'interactive_time_l',
                                                 'is_interactive', 'end_reason', 'duration', 'type', 'capabilities',
                                                 'agent_id'])

Summary = namedtuple('Summary', ['conversation_id', 'text', 'last_updated_time'])

Sdes = namedtuple('Sdes', ['customer_info_events', 'personal_info_events'])

CustomerInfo = namedtuple('CustomerInfo', ['conversation_id', 'server_time_stamp', 'customer_status', 'customer_type',
                                           'balance', 'customer_id', 'social_id', 'imei', 'user_name', 'account_name',
                                           'role', 'last_payment_year', 'last_payment_month', 'last_payment_day',
                                           'registration_year', 'registration_month', 'registration_day',
                                           'company_size', 'company_branch', 'store_zip_code', 'store_Number',
                                           'login_status', 'event_server_time_stamp', 'event_sde_type'])

PersonalInfo = namedtuple('PersonalInfo', ['conversation_id', 'server_time_stamp', 'name', 'surname', 'gender',
                                           'company', 'customer_age', 'email', 'phone', 'language',
                                           'event_server_time_stamp', 'event_sde_type'])


class ConversationHistoryRecord:
    def __init__(self, record: dict) -> None:
        # Get Info
        try:
            self.conversation_id = str(record['info']['conversationId'])
            self.info = self._parse_info(data=record['info'])
        except KeyError:
            raise ValueError('No Info event!')

        # Get Campaign
        if 'campaign' in record:
            self.campaign = self._parse_campaign(data=record['campaign'])
        else:
            self.campaign = None

        # Get Message Records
        if 'messageRecords' in record:
            self.message_records = self._parse_message_records(data=record['messageRecords'])
        else:
            self.message_records = None

        # Get Agent Participants
        if 'agentParticipants' in record:
            self.agent_participants = self._parse_agent_participants(data=record['agentParticipants'])
        else:
            self.agent_participants = None

        # Get Active Agent Participants
        if 'agentParticipantsActive' in record:
            self.agent_participants_active = self._parse_agent_participants(data=record['agentParticipantsActive'])
        else:
            self.agent_participants_active = None

        # Get Consumer Participants
        if 'consumerParticipants' in record:
            self.consumer_participants = self._parse_consumer_participants(data=record['consumerParticipants'])
        else:
            self.consumer_participants = None

        # Get Transfers
        if 'transfers' in record:
            self.transfers = self._parse_transfers(data=record['transfers'])
        else:
            self.transfers = None

        # Get Interactions
        if 'interactions' in record:
            self.interactions = self._parse_interactions(data=record['interactions'])
        else:
            self.interactions = None

        # Get Message Score
        if 'messageScores' in record:
            self.message_scores = self._parse_message_score(data=record['messageScores'])
        else:
            self.message_scores = None

        # Get Message Statuses
        if 'messageStatuses' in record:
            self.message_statuses = self._parse_message_statuses(data=record['messageStatuses'])
        else:
            self.message_statuses = None

        # Get Conversation Surveys
        if 'conversationSurveys' in record:
            self.conversation_surveys = self._parse_conversation_surveys(data=record['conversationSurveys'])
        else:
            self.conversation_surveys = None

        # Get CoBrowse Sessions
        if 'coBrowseSessions' in record:
            self.cobrowse_sessions = self._parse_cobrowse_sessions(data=record['coBrowseSessions'])
        else:
            self.cobrowse_sessions = None

        # Get Summary
        if 'summary' in record:
            self.summary = self._parse_summary(data=record['summary'])
        else:
            self.summary = None

        # Get Sdes
        if 'sdes' in record:
            self.sdes = self._parse_sdes(data=record['sdes'])
        else:
            self.sdes = None

    def _parse_info(self, data: dict) -> Info:

        return Info(
            conversation_id=self.conversation_id,
            brand_id=data['brandId'] if 'brandId' in data else None,
            status=data['status'] if 'status' in data else None,
            start_time=data['startTime'] if 'startTime' in data else None,
            start_time_l=data['startTimeL'] if 'startTimeL' in data else None,
            end_time=data['endTime'] if 'endTime' in data else None,
            end_time_l=data['endTimeL'] if 'endTimeL' in data else None,
            duration=data['duration'] if 'duration' in data else None,
            close_reason=data['closeReason'] if 'closeReason' in data else None,
            first_conversation=data['firstConversation'] if 'firstConversation' in data else None,
            csat=data['csat'] if 'csat' in data else None,
            csat_rate=data['csatRate'] if 'csatRate' in data else None,
            mcs=data['mcs'] if 'mcs' in data else None,
            alerted_mcs=data['alertedMCS'] if 'alertedMCS' in data else None,
            source=data['source'] if 'source' in data else None,
            device=data['device'] if 'device' in data else None,
            latest_skill_id=data['latestSkillId'] if 'latestSkillId' in data else None,
            latest_skill_name=data['latestSkillName'] if 'latestSkillName' in data else None,
            latest_agent_id=data['latestAgentId'] if 'latestAgentId' in data else None,
            latest_agent_login_name=data['latestAgentLoginName'] if 'latestAgentLoginName' in data else None,
            latest_agent_nickname=data['latestAgentNickname'] if 'latestAgentNickname' in data else None,
            latest_agent_full_name=data['latestAgentFullName'] if 'latestAgentFullName' in data else None,
            latest_agent_group_id=data['latestAgentGroupId'] if 'latestAgentGroupId' in data else None,
            latest_agent_group_name=data['latestAgentGroupName'] if 'latestAgentGroupName' in data else None,
            latest_queue_state=data['latestQueueState'] if 'latestQueueState' in data else None,
            browser=data['browser'] if 'browser' in data else None,
            operating_system=data['operatingSystem'] if 'operatingSystem' in data else None,
            is_partial=data['isPartial'] if 'isPartial' in data else None
        )

    def _parse_campaign(self, data: dict) -> Campaign:

        return Campaign(
            conversation_id=self.conversation_id,
            campaign_engagement_id=data['campaignEngagementId'] if 'campaignEngagementId' in data else None,
            campaign_engagement_name=data['campaignEngagementName'] if 'campaignEngagementName' in data else None,
            campaign_id=data['campaignId'] if 'campaignId' in data else None,
            campaign_name=data['campaignName'] if 'campaignName' in data else None,
            goal_id=data['goalId'] if 'goalId' in data else None,
            goal_name=data['goalName'] if 'goalName' in data else None,
            engagement_agent_note=data['engagementAgentNote'] if 'engagementAgentNote' in data else None,
            engagement_source=data['engagementSource'] if 'engagementSource' in data else None,
            visitor_behavior_id=data['visitorBehaviorId'] if 'visitorBehaviorId' in data else None,
            visitor_behavior_name=data['visitorBehaviorName'] if 'visitorBehaviorName' in data else None,
            engagement_application_id=data['engagementApplicationId'] if 'engagementApplicationId' in data else None,
            engagement_application_name=data[
                'engagementApplicationName'] if 'engagementApplicationName' in data else None,
            engagement_application_type_id=data[
                'engagementApplicationTypeId'] if 'engagementApplicationTypeId' in data else None,
            engagement_application_type_name=data[
                'engagementApplicationTypeName'] if 'engagementApplicationTypeName' in data else None,
            visitor_profile_id=data['visitorProfileId'] if 'visitorProfileId' in data else None,
            visitor_profile_name=data['visitorProfileName'] if 'visitorProfileName' in data else None,
            lob_id=data['lobId'] if 'lobId' in data else None,
            lob_name=data['lobName'] if 'lobName' in data else None,
            location_id=data['LocationId'] if 'LocationId' in data else None,
            location_name=data['LocationName'] if 'LocationName' in data else None,
            behavior_system_default=data['behaviorSystemDefault'] if 'behaviorSystemDefault' in data else None,
            profile_system_default=data['profileSystemDefault'] if 'profileSystemDefault' in data else None
        )

    def _parse_message_records(self, data: dict) -> List[Message]:
        # TODO: Parse context data (contains context data, structured metadata, bot response, intent, and action reason)

        return [Message(
            conversation_id=self.conversation_id,
            time=item['time'] if 'time' in item else None,
            time_l=item['timeL'] if 'timeL' in item else None,
            type=item['type'] if 'type' in item else None,
            message_data=item['messageData']['msg']['text'] if 'messageData' in item else None,
            message_id=item['messageId'] if 'messageId' in item else None,
            seq=item['seq'] if 'seq' in item else None,
            dialog_id=item['dialogId'] if 'dialogId' in item else None,
            participant_id=item['participantId'] if 'participantId' in item else None,
            source=item['source'] if 'source' in item else None,
            device=item['device'] if 'device' in item else None,
            sent_by=item['sentBy'] if 'sentBy' in item else None,
            context_data=item['contextData'] if 'contextData' in item else None
        ) for item in data]

    def _parse_agent_participants(self, data: dict) -> List[AgentParticipant]:

        return [AgentParticipant(
            conversation_id=self.conversation_id,
            agent_id=item['agentId'] if 'agentId' in item else None,
            agent_login_name=item['agentLoginName'] if 'agentLoginName' in item else None,
            agent_nickname=item['agentNickname'] if 'agentNickname' in item else None,
            agent_full_name=item['agentFullName'] if 'agentFullName' in item else None,
            agent_deleted=item['agentDeleted'] if 'agentDeleted' in item else None,
            time=item['time'] if 'time' in item else None,
            time_l=item['timeL'] if 'timeL' in item else None,
            role=item['role'] if 'role' in item else None,
            user_type=item['userType'] if 'userType' in item else None,
            user_type_name=item['userTypeName'] if 'userTypeName' in item else None,
            agent_group_id=item['agentGroupId'] if 'agentGroupId' in item else None,
            agent_group_name=item['agentGroupName'] if 'agentGroupName' in item else None,
            permission=item['permission'] if 'permission' in item else None
        ) for item in data]

    def _parse_consumer_participants(self, data: dict) -> List[ConsumerParticipant]:

        return [ConsumerParticipant(
            conversation_id=self.conversation_id,
            participant_id=item['participantId'] if 'participantId' in item else None,
            time=item['time'] if 'time' in item else None,
            time_l=item['timeL'] if 'timeL' in item else None,
            first_name=item['firstName'] if 'firstName' in item else None,
            last_name=item['lastName'] if 'lastName' in item else None,
            phone=item['phone'] if 'phone' in item else None,
            email=item['email'] if 'email' in item else None,
            token=item['token'] if 'token' in item else None
        ) for item in data]

    def _parse_transfers(self, data: dict) -> List[Transfer]:

        return [Transfer(
            conversation_id=self.conversation_id,
            time=item['time'] if 'time' in item else None,
            timeL=item['timeL'] if 'timeL' in item else None,
            assignedAgentId=item['assignedAgentId'] if 'assignedAgentId' in item else None,
            assignedAgentLoginName=item['assignedAgentLoginName'] if 'assignedAgentLoginName' in item else None,
            assignedAgentNickname=item['assignedAgentNickname'] if 'assignedAgentNickname' in item else None,
            assignedAgentFullName=item['assignedAgentFullName'] if 'assignedAgentFullName' in item else None,
            targetSkillId=item['targetSkillId'] if 'targetSkillId' in item else None,
            targetSkillName=item['targetSkillName'] if 'targetSkillName' in item else None,
            sourceSkillId=item['sourceSkillId'] if 'sourceSkillId' in item else None,
            sourceSkillName=item['sourceSkillName'] if 'sourceSkillName' in item else None,
            sourceAgentId=item['sourceAgentId'] if 'sourceAgentId' in item else None,
            sourceAgentLoginName=item['sourceAgentLoginName'] if 'sourceAgentLoginName' in item else None,
            sourceAgentNickname=item['sourceAgentNickname'] if 'sourceAgentNickname' in item else None,
            sourceAgentFullName=item['sourceAgentFullName'] if 'sourceAgentFullName' in item else None,
            reason=item['reason'] if 'reason' in item else None,
            # TODO: Parse context data.
            contextData=item['contextData'] if 'contextData' in item else None
        ) for item in data]

    def _parse_interactions(self, data: dict) -> List[Interaction]:

        return [Interaction(
            conversation_id=self.conversation_id,
            assigned_agent_id=item['assignedAgentId'] if 'assignedAgentId' in item else None,
            agent_login_name=item['agentLoginName'] if 'agentLoginName' in item else None,
            agent_nickname=item['agentNickname'] if 'agentFullName' in item else None,
            agent_full_name=item['interactionTime'] if 'interactionTime' in item else None,
            interaction_time=item['interactionTime'] if 'interactionTime' in item else None,
            interaction_time_l=item['interactionTimeL'] if 'interactionTimeL' in item else None,
            interactive_sequence=item['interactiveSequence'] if 'interactiveSequence' in item else None
        ) for item in data]

    def _parse_message_score(self, data: dict) -> List[MessageScore]:

        return [MessageScore(
            conversation_id=self.conversation_id,
            message_id=item['messageId'] if 'messageId' in item else None,
            time=item['time'] if 'time' in item else None,
            time_l=item['timeL'] if 'timeL' in item else None,
            mcs=item['mcs'] if 'mcs' in item else None,
            message_raw_score=item['messageRawScore'] if 'messageRawScore' in item else None
        ) for item in data]

    def _parse_message_statuses(self, data: dict) -> List[MessageStatus]:

        return [MessageStatus(
            conversation_id=self.conversation_id,
            message_delivery_status=item['messageDeliveryStatus'] if 'messageDeliveryStatus' in item else None,
            message_id=item['messageId'] if 'messageId' in item else None,
            participant_id=item['participantId'] if 'participantId' in item else None,
            participant_type=item['participantType'] if 'participantType' in item else None,
            seq=item['seq'] if 'seq' in item else None,
            time=item['time'] if 'time' in item else None,
            time_l=item['timeL'] if 'timeL' in item else None
        ) for item in data]

    def _parse_conversation_surveys(self, data: dict) -> List[Survey]:

        surveys = []
        for survey in data:
            survey_type = survey['surveyType'] if 'surveyType' in survey else None
            survey_status = survey['surveyType'] if 'surveyType' in survey else None

            if 'survey_data' in survey:
                for survey_data in survey['survey_data']:
                    surveys.append(
                        Survey(
                            conversation_id=self.conversation_id,
                            survey_type=survey_type,
                            survey_status=survey_status,
                            survey_question=survey_data['question'] if 'question' in survey_data else None,
                            survey_data=survey_data['answer'] if 'answer' in survey else None
                        )
                    )
            else:
                surveys.append(
                    Survey(
                        conversation_id=self.conversation_id,
                        survey_type=survey_type,
                        survey_status=survey_status,
                        survey_question=None,
                        survey_data=None
                    )
                )
        return surveys

    def _parse_cobrowse_sessions(self, data: dict) -> List[CoBrowseSession]:

        return [CoBrowseSession(
            conversation_id=self.conversation_id,
            session_id=item['sessionId'] if 'sessionId' in item else None,
            start_time=item['startTime'] if 'startTime' in item else None,
            start_time_l=item['startTimeL'] if 'startTimeL' in item else None,
            end_time=item['endTime'] if 'endTime' in item else None,
            end_time_l=item['endTimeL'] if 'endTimeL' in item else None,
            interactive_time=item['interactiveTime'] if 'interactiveTime' in item else None,
            interactive_time_l=item['interactiveTimeL'] if 'interactiveTimeL' in item else None,
            is_interactive=item['isInteractive'] if 'isInteractive' in item else None,
            end_reason=item['endReason'] if 'endReason' in item else None,
            duration=item['duration'] if 'duration' in item else None,
            type=item['type'] if 'type' in item else None,
            capabilities=item['capabilities'] if 'capabilities' in item else None,
            agent_id=item['agentId'] if 'agentId' in item else None
        ) for item in data['coBrowseSessionsList']]

    def _parse_summary(self, data: dict) -> Summary:

        return Summary(
            conversation_id=self.conversation_id,
            text=data['text'] if 'text' in data else None,
            last_updated_time=data['lastUpdatedTime'] if 'lastUpdatedTime' in data else None
        )

    def _parse_sdes(self, data: dict) -> Sdes:

        def filter_customer_info(event_data):
            c_info = event_data['customerInfo']['customerInfo']

            # Bread down last payment date
            if 'lastPaymentDate' in c_info:
                lpd = c_info['lastPaymentDate']
                last_payment_year = lpd['year'] if 'year' in lpd else None
                last_payment_month = lpd['month'] if 'month' in lpd else None
                last_payment_day = lpd['day'] if 'day' in lpd else None
            else:
                last_payment_year = None
                last_payment_month = None
                last_payment_day = None

            # Break down registration date
            if 'registrationDate' in c_info:
                rd = c_info['registrationDate']
                registration_year = rd['year'] if 'year' in rd else None
                registration_month = rd['month'] if 'month' in rd else None
                registration_day = rd['day'] if 'day' in rd else None
            else:
                registration_year = None
                registration_month = None
                registration_day = None

            # Get time stamp from inside customer info
            if 'serverTimeStamp' in event['customerInfo']:
                server_time_stamp = event['customerInfo']['serverTimeStamp']
            else:
                server_time_stamp = None

            return CustomerInfo(
                conversation_id=self.conversation_id,
                server_time_stamp=server_time_stamp,
                customer_status=c_info['customerStatus'] if 'customerStatus' in c_info else None,
                customer_type=c_info['customerType'] if 'customerType' in c_info else None,
                balance=c_info['balance'] if 'balance' in c_info else None,
                customer_id=c_info['customerId'] if 'customerId' in c_info else None,
                social_id=c_info['socialId'] if 'socialId' in c_info else None,
                imei=c_info['imei'] if 'imei' in c_info else None,
                user_name=c_info['userName'] if 'userName' in c_info else None,
                account_name=c_info['accountName'] if 'accountName' in c_info else None,
                role=c_info['role'] if 'role' in c_info else None,
                last_payment_year=last_payment_year,
                last_payment_month=last_payment_month,
                last_payment_day=last_payment_day,
                registration_year=registration_year,
                registration_month=registration_month,
                registration_day=registration_day,
                company_size=c_info['companySize'] if 'companySize' in c_info else None,
                company_branch=c_info['companyBranch'] if 'companyBranch' in c_info else None,
                store_zip_code=c_info['storeZipCode'] if 'storeZipCode' in c_info else None,
                store_Number=c_info['storeNumber'] if 'storeNumber' in c_info else None,
                login_status=c_info['loginStatus'] if 'loginStatus' in c_info else None,
                event_server_time_stamp=event_data['serverTimeStamp'],
                event_sde_type=event_data['sdeType']
            )

        def filter_personal_info(event_data):
            p_info = event_data['personalInfo']['personalInfo']

            # Get time stamp from inside personal info
            if 'serverTimeStamp' in event['personalInfo']:
                server_time_stamp = event['personalInfo']['serverTimeStamp']
            else:
                server_time_stamp = None

            return PersonalInfo(
                conversation_id=self.conversation_id,
                server_time_stamp=server_time_stamp,
                name=p_info['name'] if 'name' in p_info else None,
                surname=p_info['surname'] if 'surname' in p_info else None,
                gender=p_info['gender'] if 'gender' in p_info else None,
                company=p_info['company'] if 'company' in p_info else None,
                customer_age=p_info['customerAge'] if 'customerAge' in p_info else None,
                email=p_info['email'] if 'email' in p_info else None,
                phone=p_info['phone'] if 'phone' in p_info else None,
                language=p_info[''] if '' in p_info else None,
                event_server_time_stamp=event_data['serverTimeStamp'],
                event_sde_type=event_data['sdeType']
            )

        customer_info_events = []
        personal_info_events = []

        for event in data['events']:
            if 'customerInfo' in event:
                customer_info_events.append(filter_customer_info(event))
            elif 'personalInfo' in event:
                personal_info_events.append(filter_personal_info(event))

        # If events list is empty, then make variable None
        if not customer_info_events:
            customer_info_events = None

        # If events list is empty, then make variable None
        if not personal_info_events:
            personal_info_events = None

        return Sdes(
            customer_info_events=customer_info_events,
            personal_info_events=personal_info_events
        )
