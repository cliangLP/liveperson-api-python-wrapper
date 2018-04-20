"""
Provides a Data Structure for a Conversation History Record from the Messaging Interactions API.
"""

from collections import namedtuple
from typing import List

# Declare new types to store each event from data.
Info = namedtuple(
    typename='Info',
    field_names=['conversation_id', 'agent_deleted', 'alerted_mcs', 'brand_id', 'browser', 'close_reason',
                 'close_reason_description', 'csat', 'csat_rate', 'device', 'duration', 'end_time', 'end_time_l',
                 'first_conversation', 'is_partial', 'latest_agent_full_name', 'latest_agent_group_id',
                 'latest_agent_group_name', 'latest_agent_id', 'latest_agent_login_name', 'latest_agent_nickname',
                 'latest_queue_state', 'latest_skill_id', 'latest_skill_name', 'mcs', 'operating_system', 'source',
                 'start_time', 'start_time_l', 'status']
)

Campaign = namedtuple(
    typename='Campaign',
    field_names=['conversation_id', 'behavior_system_default', 'campaign_engagement_id', 'campaign_engagement_name',
                 'campaign_id', 'campaign_name', 'engagement_agent_note', 'engagement_application_id',
                 'engagement_application_name', 'engagement_application_type_id', 'engagement_application_type_name',
                 'engagement_source', 'goal_id', 'goal_name', 'lob_id', 'lob_name', 'location_id', 'location_name',
                 'profile_system_default', 'visitor_behavior_id', 'visitor_behavior_name', 'visitor_profile_id',
                 'visitor_profile_name']
)

MessageRecord = namedtuple(
    typename='MessageRecord',
    field_names=['conversation_id', 'context_data', 'device', 'dialog_id', 'message_data', 'message_id',
                 'participant_id', 'sent_by', 'seq', 'source', 'time', 'time_l', 'type']
)

AgentParticipant = namedtuple(
    typename='AgentParticipant',
    field_names=['conversation_id', 'agent_deleted', 'agent_full_name', 'agent_group_id', 'agent_group_name',
                 'agent_id', 'agent_login_name', 'agent_nickname', 'agent_pid', 'permission', 'role', 'time', 'time_l',
                 'user_type', 'user_type_name']
)

ConsumerParticipant = namedtuple(
    typename='ConsumerParticipant',
    field_names=['conversation_id', 'avatar_url', 'consumer_name', 'email', 'first_name', 'last_name', 'participant_id',
                 'phone', 'time', 'time_l', 'token']
)

Transfer = namedtuple(
    typename='Transfer',
    field_names=['conversation_id', 'assigned_agent_full_name', 'assigned_agent_id', 'assigned_agent_login_name',
                 'assigned_agent_nickname', 'by', 'context_data', 'reason', 'source_agent_full_name', 'source_agent_id',
                 'source_agent_login_name', 'source_agent_nickname', 'source_skill_id', 'source_skill_name',
                 'target_skill_id', 'target_skill_name', 'time', 'time_l']
)

Interaction = namedtuple(
    typename='Interaction',
    field_names=['conversation_id', 'assigned_agent_id', 'assigned_agent_login_name', 'assigned_agent_nickname',
                 'assigned_agent_full_name', 'interaction_time', 'interaction_time_l', 'interactive_sequence']
)

MessageScore = namedtuple(
    typename='MessageScore',
    field_names=['conversation_id', 'mcs', 'message_id', 'message_raw_score', 'time', 'time_l']
)

MessageStatus = namedtuple(
    typename='MessageStatus',
    field_names=['conversation_id', 'message_delivery_status', 'message_id', 'participant_id', 'participant_type',
                 'seq', 'time', 'time_l']
)

Survey = namedtuple(
    typename='Survey',
    field_names=['conversation_id', 'survey_answer', 'survey_question', 'survey_status', 'survey_type']
)

CoBrowseSession = namedtuple(
    typename='CoBrowseSession',
    field_names=['conversation_id', 'agent_id', 'capabilities', 'duration', 'end_reason', 'end_time', 'end_time_l',
                 'interactive_time', 'interactive_time_l', 'is_interactive', 'session_id', 'start_time',
                 'start_time_l', 'type']
)

Summary = namedtuple(
    typename='Summary',
    field_names=['conversation_id', 'last_updated_time', 'text']
)

CustomerInfo = namedtuple(
    typename='CustomerInfo',
    field_names=['conversation_id', 'account_name', 'balance', 'company_branch', 'company_size', 'customer_id',
                 'customer_status', 'customer_type', 'event_sde_type', 'event_server_time_stamp', 'imei',
                 'last_payment_day', 'last_payment_month', 'last_payment_year', 'login_status', 'registration_day',
                 'registration_month', 'registration_year', 'role', 'server_time_stamp', 'social_id', 'store_number',
                 'store_zip_code', 'user_name']
)

PersonalInfo = namedtuple(
    typename='PersonalInfo',
    field_names=['conversation_id', 'company', 'customer_age', 'email', 'event_sde_type', 'event_server_time_stamp',
                 'gender', 'language', 'name', 'phone', 'server_time_stamp', 'surname']
)


class Conversations:
    def __init__(self):
        self.info: List[Info] = []
        self.campaign: List[Campaign] = []
        self.message_record: List[MessageRecord] = []
        self.agent_participant: List[AgentParticipant] = []
        self.agent_participant_active: List[AgentParticipant] = []
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
                    self.info.append(
                        self._set_info(info_data=data, conversation_id=cid)
                    )
                elif event == 'campaign':
                    self.campaign.append(
                        self._set_campaign(campaign_data=data, conversation_id=cid)
                    )
                elif event == 'messageRecords':
                    self.message_record.extend(
                        self._set_message_records(message_record_data=data, conversation_id=cid)
                    )
                elif event == 'agentParticipants':
                    self.agent_participant.extend(
                        self._set_agent_participants(agent_participant_data=data, conversation_id=cid)
                    )
                elif event == 'agentParticipantsActive':
                    self.agent_participant_active.extend(
                        self._set_agent_participants(agent_participant_data=data, conversation_id=cid)
                    )
                elif event == 'consumerParticipants':
                    self.consumer_participant.extend(
                        self._set_consumer_participants(consumer_participant_data=data, conversation_id=cid)
                    )
                elif event == 'transfers':
                    self.transfer.extend(
                        self._set_transfers(transfer_data=data, conversation_id=cid)
                    )
                elif event == 'interactions':
                    self.interaction.extend(
                        self._set_interactions(interaction_data=data, conversation_id=cid)
                    )
                elif event == 'messageScores':
                    self.message_score.extend(
                        self._set_message_scores(message_score_data=data, conversation_id=cid)
                    )
                elif event == 'messageStatuses':
                    self.message_status.extend(
                        self._set_message_statuses(message_status_data=data, conversation_id=cid)
                    )
                elif event == 'conversationSurveys':
                    self.survey.extend(
                        self._set_surveys(survey_data=data, conversation_id=cid)
                    )
                elif event == 'coBrowseSessions':
                    self.cobrowse_session.extend(
                        self._set_cobrowse_sessions(cobrowse_session_data=data, conversation_id=cid)
                    )
                elif event == 'summary':
                    self.summary.append(
                        self._set_summary(summary_data=data, conversation_id=cid)
                    )
                elif event == 'sdes':
                    if 'events' in data:
                        customer_info, personal_info = self._set_sdes(sde_data=data['events'], conversation_id=cid)
                        if customer_info:
                            self.customer_info.extend(customer_info)
                        if personal_info:
                            self.personal_info.extend(personal_info)

    @staticmethod
    def _set_info(info_data: dict, conversation_id: str) -> Info:

        agent_deleted = None
        alerted_mcs = None
        brand_id = None
        browser = None
        close_reason = None
        close_reason_description = None
        csat = None
        csat_rate = None
        device = None
        duration = None
        end_time = None
        end_time_l = None
        first_conversation = None
        is_partial = None
        latest_agent_full_name = None
        latest_agent_group_id = None
        latest_agent_group_name = None
        latest_agent_id = None
        latest_agent_login_name = None
        latest_agent_nickname = None
        latest_queue_state = None
        latest_skill_id = None
        latest_skill_name = None
        mcs = None
        operating_system = None
        source = None
        start_time = None
        start_time_l = None
        status = None

        for name, value in info_data.items():
            if name == 'agentDeleted':
                agent_deleted = value
            elif name == 'alertedMCS':
                alerted_mcs = value
            elif name == 'brandId':
                brand_id = value
            elif name == 'browser':
                browser = value
            elif name == 'closeReason':
                close_reason = value
            elif name == 'closeReasonDescription':
                close_reason_description = value
            elif name == 'csat':
                csat = value
            elif name == 'csatRate':
                csat_rate = value
            elif name == 'device':
                device = value
            elif name == 'duration':
                duration = value
            elif name == 'endTime':
                end_time = value
            elif name == 'endTimeL':
                end_time_l = value
            elif name == 'firstConversation':
                first_conversation = value
            elif name == 'isPartial':
                is_partial = value
            elif name == 'latestAgentFullName':
                latest_agent_full_name = value
            elif name == 'latestAgentGroupId':
                latest_agent_group_id = value
            elif name == 'latestAgentGroupName':
                latest_agent_group_name = value
            elif name == 'latestAgentId':
                latest_agent_id = value
            elif name == 'latestAgentLoginName':
                latest_agent_login_name = value
            elif name == 'latestAgentNickname':
                latest_agent_nickname = value
            elif name == 'latestQueueState':
                latest_queue_state = value
            elif name == 'latestSkillId':
                latest_skill_id = value
            elif name == 'latestSkillName':
                latest_skill_name = value
            elif name == 'mcs':
                mcs = value
            elif name == 'operatingSystem':
                operating_system = value
            elif name == 'source':
                source = value
            elif name == 'startTime':
                start_time = value
            elif name == 'startTimeL':
                start_time_l = value
            elif name == 'status':
                status = value

        return Info(conversation_id=conversation_id, agent_deleted=agent_deleted, alerted_mcs=alerted_mcs,
                    brand_id=brand_id, browser=browser, close_reason=close_reason,
                    close_reason_description=close_reason_description, csat=csat, csat_rate=csat_rate,
                    device=device, duration=duration, end_time=end_time, end_time_l=end_time_l,
                    first_conversation=first_conversation, is_partial=is_partial,
                    latest_agent_full_name=latest_agent_full_name, latest_agent_group_id=latest_agent_group_id,
                    latest_agent_group_name=latest_agent_group_name, latest_agent_id=latest_agent_id,
                    latest_agent_login_name=latest_agent_login_name, latest_agent_nickname=latest_agent_nickname,
                    latest_queue_state=latest_queue_state, latest_skill_id=latest_skill_id,
                    latest_skill_name=latest_skill_name, mcs=mcs, operating_system=operating_system, source=source,
                    start_time=start_time, start_time_l=start_time_l, status=status)

    @staticmethod
    def _set_campaign(campaign_data: dict, conversation_id: str) -> Campaign:

        behavior_system_default = None
        campaign_engagement_id = None
        campaign_engagement_name = None
        campaign_id = None
        campaign_name = None
        engagement_agent_note = None
        engagement_application_id = None
        engagement_application_name = None
        engagement_application_type_id = None
        engagement_application_type_name = None
        engagement_source = None
        goal_id = None
        goal_name = None
        lob_id = None
        lob_name = None
        location_id = None
        location_name = None
        profile_system_default = None
        visitor_behavior_id = None
        visitor_behavior_name = None
        visitor_profile_id = None
        visitor_profile_name = None

        for name, value in campaign_data.items():
            if name == 'behaviorSystemDefault':
                behavior_system_default = value
            elif name == 'campaignEngagementId':
                campaign_engagement_id = value
            elif name == 'campaignEngagementName':
                campaign_engagement_name = value
            elif name == 'campaignId':
                campaign_id = value
            elif name == 'campaignName':
                campaign_name = value
            elif name == 'engagementAgentNote':
                engagement_agent_note = value
            elif name == 'engagementApplicationId':
                engagement_application_id = value
            elif name == 'engagementApplicationName':
                engagement_application_name = value
            elif name == 'engagementApplicationTypeId':
                engagement_application_type_id = value
            elif name == 'engagementApplicationTypeName':
                engagement_application_type_name = value
            elif name == 'engagementSource':
                engagement_source = value
            elif name == 'goalId':
                goal_id = value
            elif name == 'goalName':
                goal_name = value
            elif name == 'lobId':
                lob_id = value
            elif name == 'lobName':
                lob_name = value
            elif name == 'LocationId':
                location_id = value
            elif name == 'LocationName':
                location_name = value
            elif name == 'profileSystemDefault':
                profile_system_default = value
            elif name == 'visitorBehaviorId':
                visitor_behavior_id = value
            elif name == 'visitorBehaviorName':
                visitor_behavior_name = value
            elif name == 'visitorProfileId':
                visitor_profile_id = value
            elif name == 'visitorProfileName':
                visitor_profile_name = value

        return Campaign(conversation_id=conversation_id, behavior_system_default=behavior_system_default,
                        campaign_engagement_id=campaign_engagement_id,
                        campaign_engagement_name=campaign_engagement_name, campaign_id=campaign_id,
                        campaign_name=campaign_name, engagement_agent_note=engagement_agent_note,
                        engagement_application_id=engagement_application_id,
                        engagement_application_name=engagement_application_name,
                        engagement_application_type_id=engagement_application_type_id,
                        engagement_application_type_name=engagement_application_type_name,
                        engagement_source=engagement_source, goal_id=goal_id, goal_name=goal_name, lob_id=lob_id,
                        lob_name=lob_name, location_id=location_id, location_name=location_name,
                        profile_system_default=profile_system_default, visitor_behavior_id=visitor_behavior_id,
                        visitor_behavior_name=visitor_behavior_name, visitor_profile_id=visitor_profile_id,
                        visitor_profile_name=visitor_profile_name)

    @staticmethod
    def _set_message_records(message_record_data: dict, conversation_id: str) -> List[MessageRecord]:
        # TODO: Parse context data (contains context data, structured metadata, bot response, intent, and action reason)

        def parse_message_record(item: dict, cid: str):
            context_data = None
            device = None
            dialog_id = None
            message_data = None
            message_id = None
            participant_id = None
            sent_by = None
            seq = None
            source = None
            time = None
            time_l = None
            type = None

            for name, value in item.items():
                if name == 'contextData':
                    context_data = value
                elif name == 'device':
                    device = value
                elif name == 'dialogId':
                    dialog_id = value
                elif name == 'messageData':
                    if 'msg' in value and 'text' in value['msg']:
                        message_data = value['msg']['text']
                elif name == 'messageId':
                    message_id = value
                elif name == 'participantId':
                    participant_id = value
                elif name == 'sentBy':
                    sent_by = value
                elif name == 'seq':
                    seq = value
                elif name == 'source':
                    source = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value
                elif name == 'type':
                    type = value

            return MessageRecord(conversation_id=cid, context_data=context_data, device=device, dialog_id=dialog_id,
                                 message_data=message_data, message_id=message_id, participant_id=participant_id,
                                 sent_by=sent_by, seq=seq, source=source, time=time, time_l=time_l, type=type)

        return [parse_message_record(item=item, cid=conversation_id) for item in message_record_data]

    @staticmethod
    def _set_agent_participants(agent_participant_data: dict, conversation_id: str) -> List[AgentParticipant]:

        def parse_agent_participant(item: dict, cid: str):

            agent_deleted = None
            agent_full_name = None
            agent_group_id = None
            agent_group_name = None
            agent_id = None
            agent_login_name = None
            agent_nickname = None
            agent_pid = None
            permission = None
            role = None
            time = None
            time_l = None
            user_type = None
            user_type_name = None

            for name, value in item.items():
                if name == 'agentDeleted':
                    agent_deleted = value
                elif name == 'agentFullName':
                    agent_full_name = value
                elif name == 'agentGroupId':
                    agent_group_id = value
                elif name == 'agentGroupName':
                    agent_group_name = value
                elif name == 'agentId':
                    agent_id = value
                elif name == 'agentLoginName':
                    agent_login_name = value
                elif name == 'agentNickname':
                    agent_nickname = value
                elif name == 'agentPid':
                    agent_pid = value
                elif name == 'permission':
                    permission = value
                elif name == 'role':
                    role = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value
                elif name == 'userType':
                    user_type = value
                elif name == 'userTypeName':
                    user_type_name = value

            return AgentParticipant(conversation_id=cid, agent_deleted=agent_deleted, agent_full_name=agent_full_name,
                                    agent_group_id=agent_group_id, agent_group_name=agent_group_name, agent_id=agent_id,
                                    agent_login_name=agent_login_name, agent_nickname=agent_nickname,
                                    agent_pid=agent_pid, permission=permission, role=role, time=time, time_l=time_l,
                                    user_type=user_type, user_type_name=user_type_name)

        return [parse_agent_participant(item=item, cid=conversation_id) for item in agent_participant_data]

    @staticmethod
    def _set_consumer_participants(consumer_participant_data: dict, conversation_id: str) -> List[ConsumerParticipant]:

        def parse_consumer_participant(item: dict, cid: str):
            avatar_url = None
            consumer_name = None
            email = None
            first_name = None
            last_name = None
            participant_id = None
            phone = None
            time = None
            time_l = None
            token = None

            for name, value in item.items():
                if name == 'avatarURL':
                    avatar_url = value
                if name == 'consumerName':
                    consumer_name = value
                elif name == 'email':
                    email = value
                elif name == 'firstName':
                    first_name = value
                elif name == 'lastName':
                    last_name = value
                elif name == 'participantId':
                    participant_id = value
                elif name == 'phone':
                    phone = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value
                elif name == 'token':
                    token = value

            return ConsumerParticipant(conversation_id=cid, avatar_url=avatar_url, consumer_name=consumer_name,
                                       email=email, first_name=first_name, last_name=last_name,
                                       participant_id=participant_id, phone=phone, time=time, time_l=time_l,
                                       token=token)

        return [parse_consumer_participant(item=item, cid=conversation_id) for item in consumer_participant_data]

    @staticmethod
    def _set_transfers(transfer_data: dict, conversation_id: str) -> List[Transfer]:

        def parse_transfer(item: dict, cid: str):
            assigned_agent_full_name = None
            assigned_agent_id = None
            assigned_agent_login_name = None
            assigned_agent_nickname = None
            by = None
            context_data = None
            reason = None
            source_agent_full_name = None
            source_agent_id = None
            source_agent_login_name = None
            source_agent_nickname = None
            source_skill_id = None
            source_skill_name = None
            target_skill_id = None
            target_skill_name = None
            time = None
            time_l = None

            for name, value in item.items():
                if name == 'assignedAgentFullName':
                    assigned_agent_full_name = value
                elif name == 'assignedAgentId':
                    assigned_agent_id = value
                elif name == 'assignedAgentLoginName':
                    assigned_agent_login_name = value
                elif name == 'assignedAgentNickname':
                    assigned_agent_nickname = value
                elif name == 'by':
                    by = value
                elif name == 'contextData':
                    context_data = value
                elif name == 'reason':
                    reason = value
                elif name == 'sourceAgentFullName':
                    source_agent_full_name = value
                elif name == 'sourceAgentId':
                    source_agent_id = value
                elif name == 'sourceAgentLoginName':
                    source_agent_login_name = value
                elif name == 'sourceAgentNickname':
                    source_agent_nickname = value
                elif name == 'sourceSkillId':
                    source_skill_id = value
                elif name == 'sourceSkillName':
                    source_skill_name = value
                elif name == 'targetSkillId':
                    target_skill_id = value
                elif name == 'targetSkillName':
                    target_skill_name = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value

            return Transfer(conversation_id=cid, assigned_agent_full_name=assigned_agent_full_name,
                            assigned_agent_id=assigned_agent_id, assigned_agent_login_name=assigned_agent_login_name,
                            assigned_agent_nickname=assigned_agent_nickname, by=by, context_data=context_data,
                            reason=reason, source_agent_full_name=source_agent_full_name,
                            source_agent_id=source_agent_id, source_agent_login_name=source_agent_login_name,
                            source_agent_nickname=source_agent_nickname, source_skill_id=source_skill_id,
                            source_skill_name=source_skill_name, target_skill_id=target_skill_id,
                            target_skill_name=target_skill_name, time=time, time_l=time_l)

        return [parse_transfer(item=item, cid=conversation_id) for item in transfer_data]

    @staticmethod
    def _set_interactions(interaction_data: dict, conversation_id: str) -> List[Interaction]:

        def parse_interaction(item: dict, cid: str):

            assigned_agent_id = None
            assigned_agent_login_name = None
            assigned_agent_nickname = None
            assigned_agent_full_name = None
            interaction_time = None
            interaction_time_l = None
            interactive_sequence = None

            for name, value in item.items():
                if name == 'assignedAgentId':
                    assigned_agent_id = value
                elif name in ['assignedAgentLoginName', 'agentLoginName']:
                    assigned_agent_login_name = value
                elif name in ['assignedAgentNickname', 'agentNickname']:
                    assigned_agent_nickname = value
                elif name in ['assignedAgentFullName', 'agentFullName']:
                    assigned_agent_full_name = value
                elif name == 'interactionTime':
                    interaction_time = value
                elif name == 'interactionTimeL':
                    interaction_time_l = value
                elif name == 'interactiveSequence':
                    interactive_sequence = value

            return Interaction(conversation_id=cid, assigned_agent_id=assigned_agent_id,
                               assigned_agent_login_name=assigned_agent_login_name,
                               assigned_agent_nickname=assigned_agent_nickname,
                               assigned_agent_full_name=assigned_agent_full_name, interaction_time=interaction_time,
                               interaction_time_l=interaction_time_l, interactive_sequence=interactive_sequence)

        return [parse_interaction(item=item, cid=conversation_id) for item in interaction_data]

    @staticmethod
    def _set_message_scores(message_score_data: dict, conversation_id: str) -> List[MessageScore]:

        def parse_message_score(item: dict, cid: str):
            mcs = None
            message_id = None
            message_raw_score = None
            time = None
            time_l = None

            for name, value in item.items():
                if name == 'mcs':
                    mcs = value
                elif name == 'messageId':
                    message_id = value
                elif name == 'messageRawScore':
                    message_raw_score = value
                elif name == 'time':
                    time = value
                elif name == 'timeL':
                    time_l = value

            return MessageScore(conversation_id=cid, mcs=mcs, message_id=message_id,
                                message_raw_score=message_raw_score, time=time, time_l=time_l)

        return [parse_message_score(item=item, cid=conversation_id) for item in message_score_data]

    @staticmethod
    def _set_message_statuses(message_status_data: dict, conversation_id: str) -> List[MessageStatus]:

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

        return [parse_message_status(item=item, cid=conversation_id) for item in message_status_data]

    @staticmethod
    def _set_surveys(survey_data: dict, conversation_id: str) -> List[Survey]:

        def parse_survey(survey_event, cid):
            surveys = []

            survey_type = survey_event['surveyType'] if 'surveyType' in survey_event else None
            survey_status = survey_event['surveyStatus'] if 'surveyStatus' in survey_event else None

            if 'surveyData' in survey_event:
                for sd in survey_event['surveyData']:
                    surveys.append(
                        Survey(
                            conversation_id=cid,
                            survey_answer=sd['answer'] if 'answer' in sd else None,
                            survey_question=sd['question'] if 'question' in sd else None,
                            survey_type=survey_type,
                            survey_status=survey_status
                        )
                    )
            else:
                surveys.append(
                    Survey(
                        conversation_id=cid,
                        survey_answer=None,
                        survey_question=None,
                        survey_type=survey_type,
                        survey_status=survey_status
                    )
                )
            return surveys

        return [survey for item in survey_data for survey in parse_survey(survey_event=item, cid=conversation_id)]

    @staticmethod
    def _set_cobrowse_sessions(cobrowse_session_data: dict, conversation_id: str) -> List[CoBrowseSession]:

        def parse_cobrowse_session(item: dict, cid: str):

            agent_id = None
            capabilities = None
            duration = None
            end_reason = None
            end_time = None
            end_time_l = None
            interactive_time = None
            interactive_time_l = None
            is_interactive = None
            session_id = None
            start_time = None
            start_time_l = None
            type = None

            for name, value in item.items():
                if name == 'agentId':
                    agent_id = value
                elif name == 'capabilities':
                    capabilities = value
                elif name == 'duration':
                    duration = value
                elif name == 'endReason':
                    end_reason = value
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
                elif name == 'sessionId':
                    session_id = value
                elif name == 'startTime':
                    start_time = value
                elif name == 'startTimeL':
                    start_time_l = value
                elif name == 'type':
                    type = value

            return CoBrowseSession(conversation_id=cid, agent_id=agent_id, capabilities=capabilities,
                                   duration=duration, end_reason=end_reason, end_time=end_time, end_time_l=end_time_l,
                                   interactive_time=interactive_time, interactive_time_l=interactive_time_l,
                                   is_interactive=is_interactive, session_id=session_id, start_time=start_time,
                                   start_time_l=start_time_l, type=type)

        return [parse_cobrowse_session(item=item, cid=conversation_id) for item in cobrowse_session_data]

    @staticmethod
    def _set_summary(summary_data: dict, conversation_id: str) -> Summary:

        last_updated_time = None
        text = None

        for name, value in summary_data.items():
            if name == 'lastUpdatedTime':
                last_updated_time = value
            elif name == 'text':
                text = value

        return Summary(conversation_id=conversation_id, text=text, last_updated_time=last_updated_time)

    @staticmethod
    def _set_sdes(sde_data: dict, conversation_id: str) -> (List[CustomerInfo], List[PersonalInfo]):

        def filter_customer_info(event_data, cid):
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
                conversation_id=cid,
                account_name=c_info['accountName'] if 'accountName' in c_info else None,
                balance=c_info['balance'] if 'balance' in c_info else None,
                company_branch=c_info['companyBranch'] if 'companyBranch' in c_info else None,
                company_size=c_info['companySize'] if 'companySize' in c_info else None,
                customer_id=c_info['customerId'] if 'customerId' in c_info else None,
                customer_status=c_info['customerStatus'] if 'customerStatus' in c_info else None,
                customer_type=c_info['customerType'] if 'customerType' in c_info else None,
                event_sde_type=event_data['sdeType'],
                event_server_time_stamp=event_data['serverTimeStamp'],
                imei=c_info['imei'] if 'imei' in c_info else None,
                last_payment_day=last_payment_day,
                last_payment_month=last_payment_month,
                last_payment_year=last_payment_year,
                login_status=c_info['loginStatus'] if 'loginStatus' in c_info else None,
                registration_day=registration_day,
                registration_month=registration_month,
                registration_year=registration_year,
                role=c_info['role'] if 'role' in c_info else None,
                server_time_stamp=server_time_stamp,
                social_id=c_info['socialId'] if 'socialId' in c_info else None,
                store_number=c_info['storeNumber'] if 'storeNumber' in c_info else None,
                store_zip_code=c_info['storeZipCode'] if 'storeZipCode' in c_info else None,
                user_name=c_info['userName'] if 'userName' in c_info else None
            )

        def filter_personal_info(event_data, cid):
            p_info = event_data['personalInfo']['personalInfo']

            company = p_info['company'] if 'company' in p_info else None
            customer_age = p_info['customerAge'] if 'customerAge' in p_info else None
            email = None
            event_sde_type = event_data['sdeType']
            event_server_time_stamp = event_data['serverTimeStamp']
            gender = p_info['gender'] if 'gender' in p_info else None
            language = p_info['language'] if 'language' in p_info else None
            name = p_info['name'] if 'name' in p_info else None
            phone = None
            surname = p_info['surname'] if 'surname' in p_info else None,

            # Get time stamp from inside personal info
            if 'serverTimeStamp' in event_data['personalInfo']:
                server_time_stamp = event_data['personalInfo']['serverTimeStamp']
            else:
                server_time_stamp = None

            personal_info_rows = []
            if 'contacts' in p_info:
                for contact in p_info['contacts']:

                    email = phone = None

                    if 'personalContact' in contact:
                        if 'email' in contact['personalContact']:
                            email = contact['personalContact']['email']
                        if 'phone' in contact['personalContact']:
                            phone = contact['personalContact']['phone']

                    personal_info_rows.append(
                        PersonalInfo(conversation_id=cid, company=company, customer_age=customer_age, email=email,
                                     event_sde_type=event_sde_type, event_server_time_stamp=event_server_time_stamp,
                                     gender=gender, language=language, name=name, phone=phone,
                                     server_time_stamp=server_time_stamp, surname=surname)
                    )
            else:
                personal_info_rows.append(
                    PersonalInfo(conversation_id=cid, company=company, customer_age=customer_age, email=email,
                                 event_sde_type=event_sde_type, event_server_time_stamp=event_server_time_stamp,
                                 gender=gender, language=language, name=name, phone=phone,
                                 server_time_stamp=server_time_stamp, surname=surname)
                )

            return personal_info_rows

        customer_info_events = []
        personal_info_events = []

        for event in sde_data:
            if 'customerInfo' in event:
                customer_info_events.append(filter_customer_info(event_data=event, cid=conversation_id))
            elif 'personalInfo' in event:
                personal_info_events.extend(filter_personal_info(event_data=event, cid=conversation_id))

        return customer_info_events, personal_info_events
