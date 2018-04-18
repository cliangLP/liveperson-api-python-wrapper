"""
Provides a Data Structure for a Conversation History Record from the Messaging Interactions API.
"""

from collections import namedtuple
from typing import List

# Declare new types to store each event from data.
Info = namedtuple(
    typename='Info',
    field_names=['conversation_id', 'brand_id', 'status', 'start_time', 'start_time_l', 'end_time', 'end_time_l',
                 'duration', 'close_reason', 'first_conversation', 'csat', 'csat_rate', 'mcs', 'alerted_mcs', 'source',
                 'device', 'latest_skill_id', 'latest_skill_name', 'latest_agent_id', 'latest_agent_login_name',
                 'latest_agent_nickname', 'latest_agent_full_name', 'latest_agent_group_id', 'latest_agent_group_name',
                 'browser', 'operating_system', 'latest_queue_state', 'is_partial']
)

Campaign = namedtuple(
    typename='Campaign',
    field_names=['conversation_id', 'campaign_engagement_id', 'campaign_engagement_name', 'campaign_id',
                 'campaign_name', 'goal_id', 'goal_name', 'engagement_agent_note', 'engagement_source',
                 'visitor_behavior_id', 'visitor_behavior_name', 'engagement_application_id',
                 'engagement_application_name', 'engagement_application_type_id', 'engagement_application_type_name',
                 'visitor_profile_id', 'visitor_profile_name', 'lob_id', 'lob_name', 'location_id', 'location_name',
                 'behavior_system_default', 'profile_system_default']
)

MessageRecord = namedtuple(
    typename='MessageRecord',
    field_names=['conversation_id', 'time', 'time_l', 'type', 'message_data', 'message_id', 'seq', 'dialog_id',
                 'participant_id', 'source', 'device', 'sent_by', 'context_data']
)

AgentParticipant = namedtuple(
    typename='AgentParticipant',
    field_names=['conversation_id', 'agent_id', 'agent_login_name', 'agent_nickname', 'agent_full_name',
                 'agent_deleted', 'time', 'time_l', 'role', 'user_type', 'user_type_name', 'agent_group_id',
                 'agent_group_name', 'permission']
)

ConsumerParticipant = namedtuple(
    typename='ConsumerParticipant',
    field_names=['conversation_id', 'participant_id', 'time', 'time_l', 'first_name', 'last_name', 'phone', 'email',
                 'token']
)

Transfer = namedtuple(
    typename='Transfer',
    field_names=['conversation_id', 'time', 'time_l', 'assigned_agent_id', 'assigned_agent_login_name',
                 'assigned_agent_nickname', 'assigned_agent_full_name', 'target_skill_id', 'target_skill_name',
                 'source_skill_id', 'source_skill_name', 'source_agent_id', 'source_agent_login_name',
                 'source_agent_nickname', 'source_agent_full_name', 'reason', 'context_data']
)

Interaction = namedtuple(
    typename='Interaction',
    field_names=['conversation_id', 'assigned_agent_id', 'agent_login_name', 'agent_nickname', 'agent_full_name',
                 'interaction_time', 'interaction_time_l', 'interactive_sequence']
)

MessageScore = namedtuple(
    typename='MessageScore',
    field_names=['conversation_id', 'message_id', 'time', 'time_l', 'mcs', 'message_raw_score']
)

MessageStatus = namedtuple(
    typename='MessageStatus',
    field_names=['conversation_id', 'message_delivery_status', 'message_id', 'participant_id', 'participant_type',
                 'seq', 'time', 'time_l']
)

Survey = namedtuple(
    typename='Survey',
    field_names=['conversation_id', 'survey_type', 'survey_status', 'survey_question', 'survey_data']
)

CoBrowseSession = namedtuple(
    typename='CoBrowseSession',
    field_names=['conversation_id', 'session_id', 'start_time', 'start_time_l', 'end_time', 'end_time_l',
                 'interactive_time', 'interactive_time_l', 'is_interactive', 'end_reason', 'duration', 'type',
                 'capabilities', 'agent_id']
)

Summary = namedtuple(
    typename='Summary',
    field_names=['conversation_id', 'text', 'last_updated_time']
)

CustomerInfo = namedtuple(
    typename='CustomerInfo',
    field_names=['conversation_id', 'server_time_stamp', 'customer_status', 'customer_type', 'balance', 'customer_id',
                 'social_id', 'imei', 'user_name', 'account_name', 'role', 'last_payment_year', 'last_payment_month',
                 'last_payment_day', 'registration_year', 'registration_month', 'registration_day', 'company_size',
                 'company_branch', 'store_zip_code', 'store_number', 'login_status', 'event_server_time_stamp',
                 'event_sde_type']
)

PersonalInfo = namedtuple(
    typename='PersonalInfo',
    field_names=['conversation_id', 'server_time_stamp', 'name', 'surname', 'gender', 'company', 'customer_age',
                 'email', 'phone', 'language', 'event_server_time_stamp', 'event_sde_type']
)


class Conversations:
    def __init__(self):
        self.info: List[Info] = []
        self.campaign: List[Campaign] = []
        self.message_record: List[MessageRecord] = []
        self.agent_participant: List[AgentParticipant] = []
        self.agent_participants_active: List[AgentParticipant] = []
        self.consumer_participant: List[ConsumerParticipant] = []
        self.transfer: List[Transfer] = []
        self.interaction: List[Interaction] = []
        self.message_score: List[MessageScore] = []
        self.message_status: List[MessageStatus] = []
        self.survey: List[Survey] = []
        self.cobrowse_session: List[CoBrowseSession] = []
        self.summary: List[Summary] = []
        self.customer_info: List[CustomerInfo] = []
        self.personal_info: List[PersonalInfo] = []

    def append_records(self, records: List[dict]):
        for record in records:
            cid = record['info']['conversationId']
            for event, data in record.items():
                if event == 'info':
                    self.info.append(self._set_info(data=data, conversation_id=cid))
                elif event == 'campaign':
                    self.campaign.append(self._set_campaign(data=data, conversation_id=cid))
                elif event == 'messageRecords':
                    self.message_record.extend(self._set_message_records(data=data, conversation_id=cid))
                elif event == 'agentParticipants':
                    self.agent_participant.extend(self._set_agent_participants(data=data, conversation_id=cid))
                elif event == 'agentParticipantsActive':
                    self.agent_participants_active.extend(self._set_agent_participants(data=data, conversation_id=cid))
                elif event == 'consumerParticipants':
                    self.consumer_participant.extend(self._set_consumer_participants(data=data, conversation_id=cid))
                elif event == 'transfers':
                    self.transfer.extend(self._set_transfers(data=data, conversation_id=cid))
                elif event == 'interactions':
                    self.interaction.extend(self._set_interactions(data=data, conversation_id=cid))
                elif event == 'messageScores':
                    self.message_score.extend(self._set_message_scores(data=data, conversation_id=cid))
                elif event == 'messageStatuses':
                    self.message_status.extend(self._set_message_statuses(data=data, conversation_id=cid))
                elif event == 'conversationSurveys':
                    self.survey.extend(self._set_surveys(data=data, conversation_id=cid))
                elif event == 'coBrowseSessions':
                    self.cobrowse_session.extend(self._set_cobrowse_sessions(data=data, conversation_id=cid))
                elif event == 'summary':
                    self.summary.append(self._set_summary(data=data, conversation_id=cid))
                elif event == 'sdes':
                    customer_info, personal_info = self._set_sdes(data=data, conversation_id=cid)
                    self.customer_info.extend(customer_info)
                    self.personal_info.extend(personal_info)

    @staticmethod
    def _set_info(data: dict, conversation_id: str) -> Info:

        brand_id = None
        status = None
        start_time = None
        start_time_l = None
        end_time = None
        end_time_l = None
        duration = None
        close_reason = None
        first_conversation = None
        csat = None
        csat_rate = None
        mcs = None
        alerted_mcs = None
        source = None
        device = None
        latest_skill_id = None
        latest_skill_name = None
        latest_agent_id = None
        latest_agent_login_name = None
        latest_agent_nickname = None
        latest_agent_full_name = None
        latest_agent_group_id = None
        latest_agent_group_name = None
        latest_queue_state = None
        browser = None
        operating_system = None
        is_partial = None

        for name, value in data.items():
            if name == 'brandId':
                brand_id = value
            elif name == 'status':
                status = value
            elif name == 'startTime':
                start_time = value
            elif name == 'startTimeL':
                start_time_l = value
            elif name == 'endTime':
                end_time = value
            elif name == 'endTimeL':
                end_time_l = value
            elif name == 'duration':
                duration = value
            elif name == 'closeReason':
                close_reason = value
            elif name == 'firstConversation':
                first_conversation = value
            elif name == 'csat':
                csat = value
            elif name == 'csatRate':
                csat_rate = value
            elif name == 'mcs':
                mcs = value
            elif name == 'alertedMCS':
                alerted_mcs = value
            elif name == 'source':
                source = value
            elif name == 'device':
                device = value
            elif name == 'latestSkillId':
                latest_skill_id = value
            elif name == 'latestSkillName':
                latest_skill_name = value
            elif name == 'latestAgentId':
                latest_agent_id = value
            elif name == 'latestAgentLoginName':
                latest_agent_login_name = value
            elif name == 'latestAgentNickname':
                latest_agent_nickname = value
            elif name == 'latestAgentFullName':
                latest_agent_full_name = value
            elif name == 'latestAgentGroupId':
                latest_agent_group_id = value
            elif name == 'latestAgentGroupName':
                latest_agent_group_name = value
            elif name == 'latestQueueState':
                latest_queue_state = value
            elif name == 'browser':
                browser = value
            elif name == 'operatingSystem':
                operating_system = value
            elif name == 'isPartial':
                is_partial = value

        return Info(conversation_id=conversation_id, brand_id=brand_id, status=status, start_time=start_time,
                    start_time_l=start_time_l, end_time=end_time, end_time_l=end_time_l, duration=duration,
                    close_reason=close_reason, first_conversation=first_conversation, csat=csat, csat_rate=csat_rate,
                    mcs=mcs, alerted_mcs=alerted_mcs, source=source, device=device, latest_skill_id=latest_skill_id,
                    latest_skill_name=latest_skill_name, latest_agent_id=latest_agent_id,
                    latest_agent_login_name=latest_agent_login_name, latest_agent_nickname=latest_agent_nickname,
                    latest_agent_full_name=latest_agent_full_name, latest_agent_group_id=latest_agent_group_id,
                    latest_agent_group_name=latest_agent_group_name, latest_queue_state=latest_queue_state,
                    browser=browser, operating_system=operating_system, is_partial=is_partial)

    @staticmethod
    def _set_campaign(data: dict, conversation_id: str) -> Campaign:

        campaign_engagement_id = None
        campaign_engagement_name = None
        campaign_id = None
        campaign_name = None
        goal_id = None
        goal_name = None
        engagement_agent_note = None
        engagement_source = None
        visitor_behavior_id = None
        visitor_behavior_name = None
        engagement_application_id = None
        engagement_application_name = None
        engagement_application_type_id = None
        engagement_application_type_name = None
        visitor_profile_id = None
        visitor_profile_name = None
        lob_id = None
        lob_name = None
        location_id = None
        location_name = None
        behavior_system_default = None
        profile_system_default = None

        for name, value in data.items():
            if name == 'campaignEngagementId':
                campaign_engagement_id = value
            elif name == 'campaignEngagementId':
                campaign_engagement_id = value
            elif name == 'campaignEngagementName':
                campaign_engagement_name = value
            elif name == 'campaignId':
                campaign_id = value
            elif name == 'campaignName':
                campaign_name = value
            elif name == 'goalName':
                goal_name = value
            elif name == 'engagementAgentNote':
                engagement_agent_note = value
            elif name == 'engagementSource':
                engagement_source = value
            elif name == 'visitorBehaviorId':
                visitor_behavior_id = value
            elif name == 'visitorBehaviorName':
                visitor_behavior_name = value
            elif name == 'engagementApplicationId':
                engagement_application_id = value
            elif name == 'engagementApplicationName':
                engagement_application_name = value
            elif name == 'engagementApplicationTypeId':
                engagement_application_type_id = value
            elif name == 'engagementApplicationTypeName':
                engagement_application_type_name = value
            elif name == 'visitorProfileId':
                visitor_profile_id = value
            elif name == 'visitorProfileName':
                visitor_profile_name = value
            elif name == 'lobId':
                lob_id = value
            elif name == 'lobName':
                lob_name = value
            elif name == 'LocationId':
                location_id = value
            elif name == 'LocationName':
                location_name = value
            elif name == 'behaviorSystemDefault':
                behavior_system_default = value
            elif name == 'profileSystemDefault':
                profile_system_default = value

        return Campaign(conversation_id=conversation_id, campaign_engagement_id=campaign_engagement_id,
                        campaign_engagement_name=campaign_engagement_name, campaign_id=campaign_id,
                        campaign_name=campaign_name, goal_id=goal_id, goal_name=goal_name,
                        engagement_agent_note=engagement_agent_note, engagement_source=engagement_source,
                        visitor_behavior_id=visitor_behavior_id, visitor_behavior_name=visitor_behavior_name,
                        engagement_application_id=engagement_application_id,
                        engagement_application_name=engagement_application_name,
                        engagement_application_type_id=engagement_application_type_id,
                        engagement_application_type_name=engagement_application_type_name,
                        visitor_profile_id=visitor_profile_id, visitor_profile_name=visitor_profile_name, lob_id=lob_id,
                        lob_name=lob_name, location_id=location_id, location_name=location_name,
                        behavior_system_default=behavior_system_default, profile_system_default=profile_system_default)

    @staticmethod
    def _set_message_records(data: dict, conversation_id: str) -> List[MessageRecord]:
        # TODO: Parse context data (contains context data, structured metadata, bot response, intent, and action reason)

        def parse_message_record(item: dict, cid: str):
            time = None
            time_l = None
            type = None
            message_data = None
            message_id = None
            seq = None
            dialog_id = None
            participant_id = None
            source = None
            device = None
            sent_by = None
            context_data = None

            for name, value in item.items():
                if name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value
                elif name == 'type':
                    type = value
                elif name == 'messageData':
                    if 'msg' in value and 'text' in value['msg']:
                        message_data = value['msg']['text']
                elif name == 'messageId':
                    message_id = value
                elif name == 'seq':
                    seq = value
                elif name == 'dialogId':
                    dialog_id = value
                elif name == 'participantId':
                    participant_id = value
                elif name == 'source':
                    source = value
                elif name == 'device':
                    device = value
                elif name == 'sentBy':
                    sent_by = value
                elif name == 'contextData':
                    context_data = value

            return MessageRecord(conversation_id=cid, time=time, time_l=time_l, type=type,
                                 message_data=message_data, message_id=message_id, seq=seq, dialog_id=dialog_id,
                                 participant_id=participant_id, source=source, device=device, sent_by=sent_by,
                                 context_data=context_data)

        return [parse_message_record(item=item, cid=conversation_id) for item in data]

    @staticmethod
    def _set_agent_participants(data: dict, conversation_id: str) -> List[AgentParticipant]:

        def parse_agent_participant(item: dict, cid: str):
            agent_id = None
            agent_login_name = None
            agent_nickname = None
            agent_full_name = None
            agent_deleted = None
            time = None
            time_l = None
            role = None
            user_type = None
            user_type_name = None
            agent_group_id = None
            agent_group_name = None
            permission = None

            for name, value in item.items():
                if name == 'agentId':
                    agent_id = value
                elif name == 'agentLoginName':
                    agent_login_name = value
                elif name == 'agentNickname':
                    agent_nickname = value
                elif name == 'agentFullName':
                    agent_full_name = value
                elif name == 'agentDeleted':
                    agent_deleted = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value
                elif name == 'role':
                    role = value
                elif name == 'userType':
                    user_type = value
                elif name == 'userTypeName':
                    user_type_name = value
                elif name == 'agentGroupId':
                    agent_group_id = value
                elif name == 'agentGroupName':
                    agent_group_name = value
                elif name == 'permission':
                    permission = value

            return AgentParticipant(conversation_id=cid, agent_id=agent_id, agent_login_name=agent_login_name,
                                    agent_nickname=agent_nickname, agent_full_name=agent_full_name,
                                    agent_deleted=agent_deleted, time=time, time_l=time_l, role=role,
                                    user_type=user_type, user_type_name=user_type_name, agent_group_id=agent_group_id,
                                    agent_group_name=agent_group_name, permission=permission)

        return [parse_agent_participant(item=item, cid=conversation_id) for item in data]

    @staticmethod
    def _set_consumer_participants(data: dict, conversation_id: str) -> List[ConsumerParticipant]:

        def parse_consumer_participant(item: dict, cid: str):
            participant_id = None
            time = None
            time_l = None
            first_name = None
            last_name = None
            phone = None
            email = None
            token = None

            for name, value in item.items():
                if name == 'participantId':
                    participant_id = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value
                elif name == 'firstName':
                    first_name = value
                elif name == 'lastName':
                    last_name = value
                elif name == 'phone':
                    phone = value
                elif name == 'email':
                    email = value
                elif name == 'token':
                    token = value

            return ConsumerParticipant(conversation_id=cid, participant_id=participant_id, time=time, time_l=time_l,
                                       first_name=first_name, last_name=last_name, phone=phone, email=email,
                                       token=token)

        return [parse_consumer_participant(item=item, cid=conversation_id) for item in data]

    @staticmethod
    def _set_transfers(data: dict, conversation_id: str) -> List[Transfer]:

        def parse_transfer(item: dict, cid: str):
            time = None
            time_l = None
            assigned_agent_id = None
            assigned_agent_login_name = None
            assigned_agent_nickname = None
            assigned_agent_full_name = None
            target_skill_id = None
            target_skill_name = None
            source_skill_id = None
            source_skill_name = None
            source_agent_id = None
            source_agent_login_name = None
            source_agent_nickname = None
            source_agent_full_name = None
            reason = None
            context_data = None

            for name, value in item.items():
                if name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value
                elif name == 'assignedAgentId':
                    assigned_agent_id = value
                elif name == 'assignedAgentLoginName':
                    assigned_agent_login_name = value
                elif name == 'assignedAgentNickname':
                    assigned_agent_nickname = value
                elif name == 'assignedAgentFullName':
                    assigned_agent_full_name = value
                elif name == 'targetSkillId':
                    target_skill_id = value
                elif name == 'targetSkillName':
                    target_skill_name = value
                elif name == 'sourceSkillId':
                    source_skill_id = value
                elif name == 'sourceSkillName':
                    source_skill_name = value
                elif name == 'sourceAgentId':
                    source_agent_id = value
                elif name == 'sourceAgentLoginName':
                    source_agent_login_name = value
                elif name == 'sourceAgentNickname':
                    source_agent_nickname = value
                elif name == 'sourceAgentFullName':
                    source_agent_full_name = value
                elif name == 'reason':
                    reason = value
                elif name == 'contextData':
                    context_data = value

            return Transfer(conversation_id=cid, time=time, time_l=time_l, assigned_agent_id=assigned_agent_id,
                            assigned_agent_login_name=assigned_agent_login_name,
                            assigned_agent_nickname=assigned_agent_nickname,
                            assigned_agent_full_name=assigned_agent_full_name, target_skill_id=target_skill_id,
                            target_skill_name=target_skill_name, source_skill_id=source_skill_id,
                            source_skill_name=source_skill_name, source_agent_id=source_agent_id,
                            source_agent_login_name=source_agent_login_name,
                            source_agent_nickname=source_agent_nickname, source_agent_full_name=source_agent_full_name,
                            reason=reason, context_data=context_data)

        return [parse_transfer(item=item, cid=conversation_id) for item in data]

    @staticmethod
    def _set_interactions(data: dict, conversation_id: str) -> List[Interaction]:

        def parse_interaction(item: dict, cid: str):

            assigned_agent_id = None
            agent_login_name = None
            agent_nickname = None
            agent_full_name = None
            interaction_time = None
            interaction_time_l = None
            interactive_sequence = None

            for name, value in item.items():
                if name == 'assignedAgentId':
                    assigned_agent_id = value
                elif name == 'agentLoginName':
                    agent_login_name = value
                elif name == 'agentNickname':
                    agent_nickname = value
                elif name == 'agentFullName':
                    agent_full_name = value
                elif name == 'interactionTime':
                    interaction_time = value
                elif name == 'interactionTimeL':
                    interaction_time_l = value
                elif name == 'interactiveSequence':
                    interactive_sequence = value

            return Interaction(conversation_id=cid, assigned_agent_id=assigned_agent_id,
                               agent_login_name=agent_login_name, agent_nickname=agent_nickname,
                               agent_full_name=agent_full_name, interaction_time=interaction_time,
                               interaction_time_l=interaction_time_l, interactive_sequence=interactive_sequence)

        return [parse_interaction(item=item, cid=conversation_id) for item in data]

    @staticmethod
    def _set_message_scores(data: dict, conversation_id: str) -> List[MessageScore]:

        def parse_message_score(item: dict, cid: str):
            message_id = None
            time = None
            time_l = None
            mcs = None
            message_raw_score = None

            for name, value in item.items():
                if name == 'messageId':
                    message_id = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value
                elif name == 'mcs':
                    mcs = value
                elif name == 'messageRawScore':
                    message_raw_score = value

            return MessageScore(conversation_id=cid, message_id=message_id, time=time, time_l=time_l, mcs=mcs,
                                message_raw_score=message_raw_score)

        return [parse_message_score(item=item, cid=conversation_id) for item in data]

    @staticmethod
    def _set_message_statuses(data: dict, conversation_id: str) -> List[MessageStatus]:

        def parse_message_status(item: dict, cid: str):

            message_delivery_status = None
            message_id = None
            participant_id = None
            participant_type = None
            seq = None
            time = None
            time_l = None

            for name, value in item.items():
                if name == 'messageDeliveryStatus':
                    message_delivery_status = value
                elif name == 'messageId':
                    message_id = value
                elif name == 'participantId':
                    participant_id = value
                elif name == 'participantType':
                    participant_type = value
                elif name == 'seq':
                    seq = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value

            return MessageStatus(conversation_id=cid, message_delivery_status=message_delivery_status,
                                 message_id=message_id, participant_id=participant_id,
                                 participant_type=participant_type, seq=seq, time=time, time_l=time_l)

        return [parse_message_status(item=item, cid=conversation_id) for item in data]

    @staticmethod
    def _set_surveys(data: dict, conversation_id: str) -> List[Survey]:

        surveys = []
        for survey in data:
            survey_type = survey['surveyType'] if 'surveyType' in survey else None
            survey_status = survey['surveyType'] if 'surveyType' in survey else None

            if 'survey_data' in survey:
                for survey_data in survey['survey_data']:
                    surveys.append(
                        Survey(
                            conversation_id=conversation_id,
                            survey_type=survey_type,
                            survey_status=survey_status,
                            survey_question=survey_data['question'] if 'question' in survey_data else None,
                            survey_data=survey_data['answer'] if 'answer' in survey else None
                        )
                    )
            else:
                surveys.append(
                    Survey(
                        conversation_id=conversation_id,
                        survey_type=survey_type,
                        survey_status=survey_status,
                        survey_question=None,
                        survey_data=None
                    )
                )
        return surveys

    @staticmethod
    def _set_cobrowse_sessions(data: dict, conversation_id: str) -> List[CoBrowseSession]:

        def parse_cobrowse_session(item: dict, cid: str):

            session_id = None
            start_time = None
            start_time_l = None
            end_time = None
            end_time_l = None
            interactive_time = None
            interactive_time_l = None
            is_interactive = None
            end_reason = None
            duration = None
            type = None
            capabilities = None
            agent_id = None

            for name, value in item.items():
                if name == 'sessionId':
                    session_id = value
                elif name == 'startTime':
                    start_time = value
                elif name == 'startTimeL':
                    start_time_l = value
                elif name == 'endTime':
                    end_time = value
                elif name == 'endTimeL':
                    end_time_l = value
                elif name == 'interactiveTime':
                    interactive_time = value
                elif name == 'interactiveTimeL':
                    interactive_time_l = value
                elif name == 'isInteractive':
                    is_interactive = value
                elif name == 'endReason':
                    end_reason = value
                elif name == 'duration':
                    duration = value
                elif name == 'type':
                    type = value
                elif name == 'capabilities':
                    capabilities = value
                elif name == 'agentId':
                    agent_id = value

            return CoBrowseSession(conversation_id=cid, session_id=session_id, start_time=start_time,
                                   start_time_l=start_time_l, end_time=end_time, end_time_l=end_time_l,
                                   interactive_time=interactive_time, interactive_time_l=interactive_time_l,
                                   is_interactive=is_interactive, end_reason=end_reason, duration=duration,
                                   type=type, capabilities=capabilities, agent_id=agent_id)

        return [parse_cobrowse_session(item=item, cid=conversation_id) for item in data]

    @staticmethod
    def _set_summary(data: dict, conversation_id: str) -> Summary:
        text = None
        last_updated_time = None

        for name, value in data.items():
            if name == 'text':
                text = value
            elif name == 'lastUpdatedTime':
                last_updated_time = value

        return Summary(conversation_id=conversation_id, text=text, last_updated_time=last_updated_time)

    @staticmethod
    def _set_sdes(data: dict, conversation_id: str) -> (List[CustomerInfo], List[PersonalInfo]):

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
                conversation_id=conversation_id,
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
                store_number=c_info['storeNumber'] if 'storeNumber' in c_info else None,
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
                conversation_id=conversation_id,
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

        return customer_info_events, personal_info_events
