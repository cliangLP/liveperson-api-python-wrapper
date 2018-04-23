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
                 'customer_info_server_time_stamp', 'customer_status', 'customer_type', 'imei', 'last_payment_day',
                 'last_payment_month', 'last_payment_year', 'login_status', 'registration_day', 'registration_month',
                 'registration_year', 'role', 'sde_server_time_stamp', 'sde_type', 'social_id', 'store_number',
                 'store_zip_code', 'user_name']
)

PersonalInfo = namedtuple(
    typename='PersonalInfo',
    field_names=['conversation_id', 'company', 'customer_age', 'email', 'gender', 'language', 'name',
                 'personal_info_server_time_stamp', 'phone', 'sde_server_time_stamp', 'sde_type', 'surname']
)


class Conversations:
    def __init__(self) -> None:
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

    def append_records(self, records: List[dict]) -> None:
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
                        customer_info, personal_info = self._filter_sdes(sde_data=data['events'])
                        if customer_info:
                            self.customer_info.extend(
                                self._set_customer_info(customer_info_data=customer_info, conversation_id=cid)
                            )
                        if personal_info:
                            self.personal_info.extend(
                                self._set_personal_info(personal_info_data=personal_info, conversation_id=cid)
                            )

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

        for key, value in info_data.items():
            if key == 'agentDeleted':
                agent_deleted = value
            elif key == 'alertedMCS':
                alerted_mcs = value
            elif key == 'brandId':
                brand_id = value
            elif key == 'browser':
                browser = value
            elif key == 'closeReason':
                close_reason = value
            elif key == 'closeReasonDescription':
                close_reason_description = value
            elif key == 'csat':
                csat = value
            elif key == 'csatRate':
                csat_rate = value
            elif key == 'device':
                device = value
            elif key == 'duration':
                duration = value
            elif key == 'endTime':
                end_time = value
            elif key == 'endTimeL':
                end_time_l = value
            elif key == 'firstConversation':
                first_conversation = value
            elif key == 'isPartial':
                is_partial = value
            elif key == 'latestAgentFullName':
                latest_agent_full_name = value
            elif key == 'latestAgentGroupId':
                latest_agent_group_id = value
            elif key == 'latestAgentGroupName':
                latest_agent_group_name = value
            elif key == 'latestAgentId':
                latest_agent_id = value
            elif key == 'latestAgentLoginName':
                latest_agent_login_name = value
            elif key == 'latestAgentNickname':
                latest_agent_nickname = value
            elif key == 'latestQueueState':
                latest_queue_state = value
            elif key == 'latestSkillId':
                latest_skill_id = value
            elif key == 'latestSkillName':
                latest_skill_name = value
            elif key == 'mcs':
                mcs = value
            elif key == 'operatingSystem':
                operating_system = value
            elif key == 'source':
                source = value
            elif key == 'startTime':
                start_time = value
            elif key == 'startTimeL':
                start_time_l = value
            elif key == 'status':
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

        for key, value in campaign_data.items():
            if key == 'behaviorSystemDefault':
                behavior_system_default = value
            elif key == 'campaignEngagementId':
                campaign_engagement_id = value
            elif key == 'campaignEngagementName':
                campaign_engagement_name = value
            elif key == 'campaignId':
                campaign_id = value
            elif key == 'campaignName':
                campaign_name = value
            elif key == 'engagementAgentNote':
                engagement_agent_note = value
            elif key == 'engagementApplicationId':
                engagement_application_id = value
            elif key == 'engagementApplicationName':
                engagement_application_name = value
            elif key == 'engagementApplicationTypeId':
                engagement_application_type_id = value
            elif key == 'engagementApplicationTypeName':
                engagement_application_type_name = value
            elif key == 'engagementSource':
                engagement_source = value
            elif key == 'goalId':
                goal_id = value
            elif key == 'goalName':
                goal_name = value
            elif key == 'lobId':
                lob_id = value
            elif key == 'lobName':
                lob_name = value
            elif key == 'LocationId':
                location_id = value
            elif key == 'LocationName':
                location_name = value
            elif key == 'profileSystemDefault':
                profile_system_default = value
            elif key == 'visitorBehaviorId':
                visitor_behavior_id = value
            elif key == 'visitorBehaviorName':
                visitor_behavior_name = value
            elif key == 'visitorProfileId':
                visitor_profile_id = value
            elif key == 'visitorProfileName':
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

        def parse_message_record(item: dict, cid: str) -> MessageRecord:
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

            for key, value in item.items():
                if key == 'contextData':
                    context_data = value
                elif key == 'device':
                    device = value
                elif key == 'dialogId':
                    dialog_id = value
                elif key == 'messageData':
                    if 'msg' in value and 'text' in value['msg']:
                        message_data = value['msg']['text']
                elif key == 'messageId':
                    message_id = value
                elif key == 'participantId':
                    participant_id = value
                elif key == 'sentBy':
                    sent_by = value
                elif key == 'seq':
                    seq = value
                elif key == 'source':
                    source = value
                elif key == 'time':
                    time = value
                elif key == 'timeL':
                    time_l = value
                elif key == 'type':
                    type = value

            return MessageRecord(conversation_id=cid, context_data=context_data, device=device, dialog_id=dialog_id,
                                 message_data=message_data, message_id=message_id, participant_id=participant_id,
                                 sent_by=sent_by, seq=seq, source=source, time=time, time_l=time_l, type=type)

        return [parse_message_record(item=item, cid=conversation_id) for item in message_record_data]

    @staticmethod
    def _set_agent_participants(agent_participant_data: dict, conversation_id: str) -> List[AgentParticipant]:

        def parse_agent_participant(item: dict, cid: str) -> AgentParticipant:

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

            for key, value in item.items():
                if key == 'agentDeleted':
                    agent_deleted = value
                elif key == 'agentFullName':
                    agent_full_name = value
                elif key == 'agentGroupId':
                    agent_group_id = value
                elif key == 'agentGroupName':
                    agent_group_name = value
                elif key == 'agentId':
                    agent_id = value
                elif key == 'agentLoginName':
                    agent_login_name = value
                elif key == 'agentNickname':
                    agent_nickname = value
                elif key == 'agentPid':
                    agent_pid = value
                elif key == 'permission':
                    permission = value
                elif key == 'role':
                    role = value
                elif key == 'time':
                    time = value
                elif key == 'timeL':
                    time_l = value
                elif key == 'userType':
                    user_type = value
                elif key == 'userTypeName':
                    user_type_name = value

            return AgentParticipant(conversation_id=cid, agent_deleted=agent_deleted, agent_full_name=agent_full_name,
                                    agent_group_id=agent_group_id, agent_group_name=agent_group_name, agent_id=agent_id,
                                    agent_login_name=agent_login_name, agent_nickname=agent_nickname,
                                    agent_pid=agent_pid, permission=permission, role=role, time=time, time_l=time_l,
                                    user_type=user_type, user_type_name=user_type_name)

        return [parse_agent_participant(item=item, cid=conversation_id) for item in agent_participant_data]

    @staticmethod
    def _set_consumer_participants(consumer_participant_data: dict, conversation_id: str) -> List[ConsumerParticipant]:

        def parse_consumer_participant(item: dict, cid: str) -> ConsumerParticipant:
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

            for key, value in item.items():
                if key == 'avatarURL':
                    avatar_url = value
                elif key == 'consumerName':
                    consumer_name = value
                elif key == 'email':
                    email = value
                elif key == 'firstName':
                    first_name = value
                elif key == 'lastName':
                    last_name = value
                elif key == 'participantId':
                    participant_id = value
                elif key == 'phone':
                    phone = value
                elif key == 'time':
                    time = value
                elif key == 'timeL':
                    time_l = value
                elif key == 'token':
                    token = value

            return ConsumerParticipant(conversation_id=cid, avatar_url=avatar_url, consumer_name=consumer_name,
                                       email=email, first_name=first_name, last_name=last_name,
                                       participant_id=participant_id, phone=phone, time=time, time_l=time_l,
                                       token=token)

        return [parse_consumer_participant(item=item, cid=conversation_id) for item in consumer_participant_data]

    @staticmethod
    def _set_transfers(transfer_data: dict, conversation_id: str) -> List[Transfer]:

        def parse_transfer(item: dict, cid: str) -> Transfer:
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

            for key, value in item.items():
                if key == 'assignedAgentFullName':
                    assigned_agent_full_name = value
                elif key == 'assignedAgentId':
                    assigned_agent_id = value
                elif key == 'assignedAgentLoginName':
                    assigned_agent_login_name = value
                elif key == 'assignedAgentNickname':
                    assigned_agent_nickname = value
                elif key == 'by':
                    by = value
                elif key == 'contextData':
                    context_data = value
                elif key == 'reason':
                    reason = value
                elif key == 'sourceAgentFullName':
                    source_agent_full_name = value
                elif key == 'sourceAgentId':
                    source_agent_id = value
                elif key == 'sourceAgentLoginName':
                    source_agent_login_name = value
                elif key == 'sourceAgentNickname':
                    source_agent_nickname = value
                elif key == 'sourceSkillId':
                    source_skill_id = value
                elif key == 'sourceSkillName':
                    source_skill_name = value
                elif key == 'targetSkillId':
                    target_skill_id = value
                elif key == 'targetSkillName':
                    target_skill_name = value
                elif key == 'time':
                    time = value
                elif key == 'timeL':
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

        def parse_interaction(item: dict, cid: str) -> Interaction:

            assigned_agent_id = None
            assigned_agent_login_name = None
            assigned_agent_nickname = None
            assigned_agent_full_name = None
            interaction_time = None
            interaction_time_l = None
            interactive_sequence = None

            for key, value in item.items():
                if key == 'assignedAgentId':
                    assigned_agent_id = value
                elif key in ['assignedAgentLoginName', 'agentLoginName']:
                    assigned_agent_login_name = value
                elif key in ['assignedAgentNickname', 'agentNickname']:
                    assigned_agent_nickname = value
                elif key in ['assignedAgentFullName', 'agentFullName']:
                    assigned_agent_full_name = value
                elif key == 'interactionTime':
                    interaction_time = value
                elif key == 'interactionTimeL':
                    interaction_time_l = value
                elif key == 'interactiveSequence':
                    interactive_sequence = value

            return Interaction(conversation_id=cid, assigned_agent_id=assigned_agent_id,
                               assigned_agent_login_name=assigned_agent_login_name,
                               assigned_agent_nickname=assigned_agent_nickname,
                               assigned_agent_full_name=assigned_agent_full_name, interaction_time=interaction_time,
                               interaction_time_l=interaction_time_l, interactive_sequence=interactive_sequence)

        return [parse_interaction(item=item, cid=conversation_id) for item in interaction_data]

    @staticmethod
    def _set_message_scores(message_score_data: dict, conversation_id: str) -> List[MessageScore]:

        def parse_message_score(item: dict, cid: str) -> MessageScore:
            mcs = None
            message_id = None
            message_raw_score = None
            time = None
            time_l = None

            for key, value in item.items():
                if key == 'mcs':
                    mcs = value
                elif key == 'messageId':
                    message_id = value
                elif key == 'messageRawScore':
                    message_raw_score = value
                elif key == 'time':
                    time = value
                elif key == 'timeL':
                    time_l = value

            return MessageScore(conversation_id=cid, mcs=mcs, message_id=message_id,
                                message_raw_score=message_raw_score, time=time, time_l=time_l)

        return [parse_message_score(item=item, cid=conversation_id) for item in message_score_data]

    @staticmethod
    def _set_message_statuses(message_status_data: dict, conversation_id: str) -> List[MessageStatus]:

        def parse_message_status(item: dict, cid: str) -> MessageStatus:

            message_delivery_status = None
            message_id = None
            participant_id = None
            participant_type = None
            seq = None
            time = None
            time_l = None

            for key, value in item.items():
                if key == 'messageDeliveryStatus':
                    message_delivery_status = value
                elif key == 'messageId':
                    message_id = value
                elif key == 'participantId':
                    participant_id = value
                elif key == 'participantType':
                    participant_type = value
                elif key == 'seq':
                    seq = value
                elif key == 'time':
                    time = value
                elif key == 'timeL':
                    time_l = value

            return MessageStatus(conversation_id=cid, message_delivery_status=message_delivery_status,
                                 message_id=message_id, participant_id=participant_id,
                                 participant_type=participant_type, seq=seq, time=time, time_l=time_l)

        return [parse_message_status(item=item, cid=conversation_id) for item in message_status_data]

    @staticmethod
    def _set_surveys(survey_data: dict, conversation_id: str) -> List[Survey]:

        def parse_survey(survey_event, cid) -> Survey:

            survey_type = None
            survey_status = None

            if 'surveyType' in survey_event and survey_event['surveyType']:
                survey_type = survey_event['surveyType']

            if 'surveyStatus' in survey_event and survey_event['surveyStatus']:
                survey_status = survey_event['surveyStatus']

            surveys = []

            if 'surveyData' in survey_event and survey_event['surveyData']:
                for sd in survey_event['surveyData']:

                    survey_answer = None
                    survey_question = None

                    if 'answer' in sd and sd['answer']:
                        survey_answer = sd['answer']

                    if 'question' in sd and sd['question']:
                        survey_question = sd['question']

                    surveys.append(
                        Survey(conversation_id=cid, survey_answer=survey_answer, survey_question=survey_question,
                               survey_type=survey_type, survey_status=survey_status)
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

        def parse_cobrowse_session(item: dict, cid: str) -> CoBrowseSession:

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

            for key, value in item.items():
                if key == 'agentId':
                    agent_id = value
                elif key == 'capabilities':
                    capabilities = value
                elif key == 'duration':
                    duration = value
                elif key == 'endReason':
                    end_reason = value
                elif key == 'endTime':
                    end_time = value
                elif key == 'endTimeL':
                    end_time_l = value
                elif key == 'interactiveTime':
                    interactive_time = value
                elif key == 'interactiveTimeL':
                    interactive_time_l = value
                elif key == 'isInteractive':
                    is_interactive = value
                elif key == 'sessionId':
                    session_id = value
                elif key == 'startTime':
                    start_time = value
                elif key == 'startTimeL':
                    start_time_l = value
                elif key == 'type':
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

        for key, value in summary_data.items():
            if key == 'lastUpdatedTime':
                last_updated_time = value
            elif key == 'text':
                text = value

        return Summary(conversation_id=conversation_id, text=text, last_updated_time=last_updated_time)

    @staticmethod
    def _filter_sdes(sde_data: dict) -> (List[dict], List[dict]):

        customer_info_events = []
        personal_info_events = []

        for event in sde_data:
            if 'customerInfo' in event and event['customerInfo']:
                customer_info_events.append(event)
            elif 'personalInfo' in event and event['personalInfo']:
                personal_info_events.append(event)

        return customer_info_events, personal_info_events

    @staticmethod
    def _set_customer_info(customer_info_data: List[dict], conversation_id: str) -> List[CustomerInfo]:

        def parse_customer_info(ci_item: dict, cid: str) -> CustomerInfo:

            account_name = None
            balance = None
            company_branch = None
            company_size = None
            customer_id = None
            customer_info_server_time_stamp = None
            customer_status = None
            customer_type = None
            imei = None
            last_payment_day = None
            last_payment_month = None
            last_payment_year = None
            login_status = None
            registration_day = None
            registration_month = None
            registration_year = None
            role = None
            sde_type = None
            sde_server_time_stamp = None
            social_id = None
            store_number = None
            store_zip_code = None
            user_name = None

            c_info = ci_item['customerInfo']['customerInfo']

            for key, value in c_info.items():
                if key == 'accountName':
                    account_name = value
                elif key == 'balance':
                    balance = value
                elif key == 'companyBranch':
                    company_branch = value
                elif key == 'companySize':
                    company_size = value
                elif key == 'customerId':
                    customer_id = value
                elif key == 'customerStatus':
                    customer_status = value
                elif key == 'customerType':
                    customer_type = value
                elif key == 'imei':
                    imei = value
                elif key == 'lastPaymentDate':
                    if 'year' in value and value['year']:
                        last_payment_year = value['year']
                    if 'month' in value and value['month']:
                        last_payment_month = value['month']
                    if 'day' in value and value['day']:
                        last_payment_day = value['day']
                elif key == 'loginStatus':
                    login_status = value
                elif key == 'registrationDate':
                    if 'year' in value and value['year']:
                        registration_year = value['year']
                    if 'month' in value and value['month']:
                        registration_month = value['month']
                    if 'day' in value and value['day']:
                        registration_day = value['day']
                elif key == 'role':
                    role = value
                elif key == 'socialId':
                    social_id = value
                elif key == 'storeNumber':
                    store_number = value
                elif key == 'storeZipCode':
                    store_zip_code = value
                elif key == 'userName':
                    user_name = value

            # SDE Type
            if 'sdeType' in ci_item and ci_item['sdeType']:
                sde_type = ci_item['sdeType']

            # SDE Server Time Stamp
            if 'serverTimeStamp' in ci_item and ci_item['serverTimeStamp']:
                sde_server_time_stamp = ci_item['serverTimeStamp']

            # Get time stamp from inside customer info
            if 'serverTimeStamp' in ci_item['customerInfo'] and ci_item['customerInfo']['serverTimeStamp']:
                customer_info_server_time_stamp = ci_item['customerInfo']['serverTimeStamp']

            return CustomerInfo(conversation_id=cid, account_name=account_name, balance=balance,
                                company_branch=company_branch, company_size=company_size, customer_id=customer_id,
                                customer_info_server_time_stamp=customer_info_server_time_stamp,
                                customer_status=customer_status, customer_type=customer_type, imei=imei,
                                last_payment_day=last_payment_day, last_payment_month=last_payment_month,
                                last_payment_year=last_payment_year, login_status=login_status,
                                registration_day=registration_day, registration_month=registration_month,
                                registration_year=registration_year, role=role, sde_type=sde_type,
                                sde_server_time_stamp=sde_server_time_stamp, social_id=social_id,
                                store_number=store_number, store_zip_code=store_zip_code, user_name=user_name)

        return [parse_customer_info(ci_item=item, cid=conversation_id) for item in customer_info_data]

    @staticmethod
    def _set_personal_info(personal_info_data: List[dict], conversation_id: str) -> List[PersonalInfo]:

        def parse_personal_info(pi_item: dict, cid: str) -> PersonalInfo:

            company = None
            customer_age = None
            gender = None
            language = None
            name = None
            personal_info_server_time_stamp = None
            sde_type = None
            sde_server_time_stamp = None
            surname = None

            p_info = pi_item['personalInfo']['personalInfo']

            for key, value in p_info.items():
                if key == 'company':
                    company = value
                elif key == 'customerAge':
                    customer_age = value
                elif key == 'gender':
                    gender = value
                elif key == 'language':
                    language = value
                elif key == 'name':
                    name = value
                elif key == 'surname':
                    surname = value

            # SDE Type
            if 'sdeType' in pi_item and pi_item['sdeType']:
                sde_type = pi_item['sdeType']

            # SDE Server Time Stamp
            if 'serverTimeStamp' in pi_item and pi_item['serverTimeStamp']:
                sde_server_time_stamp = pi_item['serverTimeStamp']

            # Get time stamp from inside customer info
            if 'serverTimeStamp' in pi_item['personalInfo'] and pi_item['personalInfo']['serverTimeStamp']:
                personal_info_server_time_stamp = pi_item['personalInfo']['serverTimeStamp']

            personal_info_rows = []

            if 'contacts' in p_info and p_info['contacts']:
                for contact in p_info['contacts']:

                    email = None
                    phone = None

                    if 'personalContact' in contact and contact['personalContact']:
                        if 'email' in contact['personalContact'] and contact['personalContact']['email']:
                            email = contact['personalContact']['email']
                        if 'phone' in contact['personalContact'] and contact['personalContact']['phone']:
                            phone = contact['personalContact']['phone']

                    personal_info_rows.append(
                        PersonalInfo(conversation_id=cid, company=company, customer_age=customer_age, email=email,
                                     gender=gender, language=language, name=name,
                                     personal_info_server_time_stamp=personal_info_server_time_stamp,
                                     phone=phone, sde_server_time_stamp=sde_server_time_stamp, sde_type=sde_type,
                                     surname=surname)
                    )
            else:
                personal_info_rows.append(
                    PersonalInfo(conversation_id=cid, company=company, customer_age=customer_age, email=None,
                                 gender=gender, language=language, name=name,
                                 personal_info_server_time_stamp=personal_info_server_time_stamp,
                                 phone=None, sde_server_time_stamp=sde_server_time_stamp, sde_type=sde_type,
                                 surname=surname)
                )

            return personal_info_rows

        return [
            personal_info
            for item in personal_info_data
            for personal_info in parse_personal_info(pi_item=item, cid=conversation_id)
        ]
