from pymongo import MongoClient
from mail_parser import mail_parser

if __name__ == '__main__':
    client = MongoClient("127.0.0.1", 27017)
    db_mail = client["db_mail"]
    collection_mail = db_mail.collection_mail

    mail_usr = "your mail"
    password = "your password"
    mails_info = mail_parser(mail_usr, password)

    collection_mail.insert_many(mails_info)

    print(collection_mail.count_documents({}))

    db_mail.drop_collection('collection_news')
    client.close()
