from flask_restx import Namespace, Resource, fields
from flask import make_response, request
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from rag import retriever
from langchain_core.output_parsers import StrOutputParser
import time

api_ns = Namespace('api', description="A namespace for apis")

chat_model = api_ns.model('ChatInput', {
    'message': fields.String(required=True)
})


@api_ns.route("/hello")
class Basic(Resource):
    def post(self):
        data = request.get_json()

        message = data.get('message')

        response = make_response(f'<div>user: {message}</div>')
        response.headers['Content-Type'] = 'text/html'
        return response


# TODO: make route streamable
# TODO: implement memory
@api_ns.route('/chat-general')
@api_ns.expect(chat_model, validate=True)
class ChatGeneral(Resource):

    def post(self):

        data = request.get_json()

        message = data.get('message')

        template = """Answer the question based on this context:
{context}

Question: {question}
"""

        prompt = ChatPromptTemplate.from_template(template)

        model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        result = chain.invoke(message)

        result = result.replace("\n", "<br/>")

        response = make_response(f"""<div style="background-color: rgba(0, 0, 0, 0.0); margin-bottom: 40px;">
    <p style="font-weight: bold; margin-bottom: 0px;">ChatCSI</p>
    <div class="typewriter">{result}</div>
</div>""")
        response.headers['Content-Type'] = 'text/html'

        return response


@api_ns.route('/chat-admissions')
@api_ns.expect(chat_model, validate=True)
class ChatAdmissions(Resource):

    def post(self):

        data = request.get_json()

        message = data.get('message')

        template = """Answer the question based on this context:
{context}

Question: {question}
"""

        prompt = ChatPromptTemplate.from_template(template)

        model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        result = chain.invoke(message)

        result = result.replace("\n", "<br/>")

        response = make_response(f"""<div style="background-color: rgba(0, 0, 0, 0.0); margin-bottom: 40px;">
    <p style="font-weight: bold; margin-bottom: 0px;">ChatCSI</p>
    <div class="typewriter">{result}</div>
</div>""")
        response.headers['Content-Type'] = 'text/html'

        return response


@api_ns.route('/chat-cs')
@api_ns.expect(chat_model, validate=True)
class ChatCs(Resource):

    def post(self):

        data = request.get_json()

        message = data.get('message')

        template = """Answer the question based on this context:
{context}

Question: {question}
"""

        prompt = ChatPromptTemplate.from_template(template)

        model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        result = chain.invoke(message)

        result = result.replace("\n", "<br/>")

        response = make_response(f"""<div style="background-color: rgba(0, 0, 0, 0.0); margin-bottom: 40px;">
    <p style="font-weight: bold; margin-bottom: 0px;">ChatCSI</p>
    <div class="typewriter">{result}</div>
</div>""")
        response.headers['Content-Type'] = 'text/html'

        return response
