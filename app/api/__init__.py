from flask_restx import Namespace, Resource, fields
from flask import make_response, request
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from rag import retriever
from langchain_core.output_parsers import StrOutputParser

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
@api_ns.route('/chat')
@api_ns.expect(chat_model, validate=True)
class Chat(Resource):
    def post(self):

        data = request.get_json()

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

        message = data.get('message')

        result = chain.invoke(message)

        print(result)

        response = make_response(f"""<div style="background-color: rgba(0, 0, 0, 0.0); margin-bottom: 20px;">
    <p style="font-weight: bold; margin-bottom: 0px;">You</p>
    <p style="margin-bottom: 0px;">{message}</p>
</div>
<div style="background-color: rgba(0, 0, 0, 0.0); margin-bottom: 40px;">
    <p style="font-weight: bold; margin-bottom: 0px;">ChatCSI</p>
    <p>{result}</p>
</div>""")
        response.headers['Content-Type'] = 'text/html'

        return response


"""
GET https://google.com
"""
