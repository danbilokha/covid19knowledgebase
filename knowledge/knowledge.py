import json

from flask import jsonify
from fuzzywuzzy import fuzz

from knowledge.tables import KnowledgeSchema, LogsSchema


class KnowledgeManager:
    def __init__(self, db):
        self.knowledgeDAL = KnowledgeDAL(db)
        self.db = db

    def get_meta_all_data(self):
        new_log = LogsSchema(
            type='GET',
            message='Getting all meta',
            info='get_meta_all_data'
        )
        try:
            self.db.session.add(new_log)
            self.db.session.commit()
        except:
            print('Could not create a log')

        return self.knowledgeDAL.get_meta_all_data()

    def get_meta_categories(self):
        new_log = LogsSchema(
            type='GET',
            message='Getting meta categories',
            info='get_meta_categories'
        )
        try:
            self.db.session.add(new_log)
            self.db.session.commit()
        except:
            print('Could not create a log')

        return self.knowledgeDAL.get_meta_categories()

    def get_all_data(self):
        new_log = LogsSchema(
            type='GET',
            message='Getting all',
            info='get_all_data'
        )
        try:
            self.db.session.add(new_log)
            self.db.session.commit()
        except:
            print('Could not create a log')

        return jsonify(self.knowledgeDAL.get_all_data().items())

    def get_answers(self, question):
        new_question_log = LogsSchema(
            type='GET ANSWER',
            message=('Getting answer for %d question' % question),
            info='get_answers'
        )
        try:
            self.db.session.add(new_question_log)
            self.db.session.commit()
        except:
            print('Could not create a log')

        answer = self.knowledgeDAL.get_answers(question)

        new_answer_log = LogsSchema(
            type='GOT ANSWER',
            message=f'Got answer for {question} question. {answer} answer',
            info='get_answers'
        )
        try:
            self.db.session.add(new_answer_log)
            self.db.session.commit()
        except:
            print('Could not create a log')

        return answer

    def add_knowledge(self,
                      question,
                      category,
                      answer,
                      countries,
                      links,
                      additional_answers,
                      additional_links,
                      ):
        return self.knowledgeDAL.add_knowlegde(
            question=question,
            category=category,
            answer=answer,
            countries=countries,
            links=links,
            additional_answers=additional_answers,
            additional_links=additional_links,
        )


class KnowledgeDAL:
    def __init__(self, db):
        self.db = db
        with open('knowledge/knowledge_metadata.json') as f:
            self.knowledgeMetaJsonData = json.load(f)
        self.arrayKnowledgeMeta = self.knowledgeMetaJsonData.items()

    def get_meta_all_data(self):
        return self.arrayKnowledgeMeta

    def get_meta_categories(self):
        results = []

        categories = self.arrayKnowledgeMeta['categories']
        for category in categories:
            results.insert(0, category)

        return results

    def get_all_data(self):
        return self.db.session.query(KnowledgeSchema).order_by(KnowledgeSchema.date_created).all()

    def get_answers(self, question):
        results = []

        for knowledge in self.db.session.query(KnowledgeSchema).all():
            if fuzz.token_set_ratio(knowledge.question, question) > 95:
                results.insert(0, knowledge)

        return results

    def add_knowlegde(self,
                      question,
                      category,
                      answer,
                      countries,
                      links,
                      additional_answers,
                      additional_links,
                      ):
        new_knowledge = KnowledgeSchema(
            question=question,
            category=category,
            answer=answer,
            countries=countries,
            links=links,
            additional_answers=additional_answers,
            additional_links=additional_links,
        )

        try:
            self.db.session.add(new_knowledge)
            self.db.session.commit()
            return 'Success'
        except:
            raise Exception('x should not exceed 5. The value of x was: {}'.format(x))


class LogsManager:
    def __init__(self, db):
        self.db = db
        self.logsDAL = LogsDAL(db)

    def add_dump(self):
        return self.logsDAL.add_dump()

    def get_all(self):
        return jsonify(self.logsDAL.get_all())


class LogsDAL:
    def __init__(self, db):
        self.db = db

    def add_dump(self):
        new_question_log = LogsSchema(
            type='DUMP',
            message=('DUMPDUMPDUMP'),
            info='DUMPDUMPDUMP'
        )
        try:
            self.db.session.add(new_question_log)
            self.db.session.commit()
        except:
            print('Could not create a log')

    def get_all(self):
        return self.db.session.query(LogsSchema).order_by(LogsSchema.date_created).all()
