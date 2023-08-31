import models, schemas
from sqlalchemy.orm import Session, join



def get_conversation_by_user_id(db:Session,user_id:int):
    return db.query(models.Conversation).join(models.Conversation_participant).filter(models.Conversation_participant.participant_id==user_id).all()

def get_conversation_by_conv_id(db:Session,conversation_id:int):
    return db.query(models.Conversation).filter(models.Conversation.conversation_id==conversation_id).first()

def get_all_conversations(db:Session):
    return db.query(models.Conversation).all()

def get_conversation_by_message_id(db:Session,message_id:int):
    return db.query(models.Conversation).join(models.Message).filter(models.Message.message_id==message_id).first()



def get_messages_by_conv_id(db:Session,conversation_id:int):
    return db.query(models.Message).filter(models.Message.conversation_id==conversation_id).all()

def get_message_by_message_id(db:Session,message_id:int):
    return db.query(models.Message).filter(models.Message.message_id==message_id).first()



def get_conversation_participants(db:Session,conversation_id:int):
    return db.query(models.User).join(models.Conversation_participant).filter(models.Conversation_participant.conversation_id==conversation_id).all()
##please check this above function wheather the joining is correct or not



def get_participants_by_message_id(db:Session, mesage_id:int):
    convo = get_conversation_by_message_id(db,mesage_id)
    return get_conversation_participants(db,convo.conversation_id)

def create_conversation(db:Session,db_conversation:models.Conversation):
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def update_conversaion(db:Session,conversation_id:int,conversation:schemas.Conversation_Update):
    values=conversation.dict(exclude_unset=True)
    db.query(models.Conversation).filter(models.Conversation.conversation_id==conversation_id) \
    .update(values,synchronize_session=False)
    db.commit()
    return get_conversation_by_conv_id(db,conversation_id)


def send_message(db:Session,db_message:models.Message):
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message 

def update_message(db:Session, message_id:int, message:schemas.Message_Update):
    values=message.dict(exclude_unset=True)
    db.query(models.Message).filter(models.Message.message_id==message_id) \
    .update(values,synchronize_session=False)
    db.commit()
    return get_message_by_message_id(db,message_id)

def add_conversation_participant(db:Session,db_conversation_participant:models.Conversation_Participant):
    db.add(db_conversation_participant)
    db.commit()
    db.refresh(db_conversation_participant)
    return db_conversation_participant  