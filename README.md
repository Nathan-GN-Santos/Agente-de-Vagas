# Agente-de-Vagas

![alt text](image-1.png)

#### Things to do
- The AI allucinates giving a match even though theres curriculum PDF uploaded to compare.
- The Buscador de Vagas Inteligentes is not working as expected yet. 

# 1. Apresentação do grupo e do problema / aprox. 45 segundos
- Aparecer na câmera e dizer seus nomes. 
- Explicar o problema que o Agente resolve com clareza.
- O público-alvo é apresentado

# 2. Demonstração ao vivo do agente funcioando / aprox. 1 min 30 seg
- Exibir tela/interface na gravação.
- Pelos menos demonstrar 2 exemplos de entrada e resposta da IA.
- Demonstrar ao vivo. Não pode ser prints.

# 3. Explicação do Fluxo Técnico / aprox. 1 minuto
- Explicar o fluxo complexo : Interface > Automação > IA > Dados
- As ferramentas usadas (Streamlit, Make, Gemini, Notion)

# 4. Exibição dos Prompts Utilizados / aprox. 30 segundos
- Exibir o prompt profissional na tela
- Explicar brevemente por que o prompt foi feito dessa forma

# 5. Análise Crítica /  aprox. 45 segundos
- Citar ao menos limitação técnica do agente
- Mencionar risco ético, de segurança  ou privacidade.
- Apresentar pelo menos uma melhoria futura

# 6. Encerramento e Entrega / aprox. 15 segundos
- Todos os integrantes aparecer no encerramento. 
- O vídeo deve ter no máximo 5 minutos.
- Deve ser públicado no youtube como não listado.
- Enviar o link até 24/05 


# Raw understanding:

O que é Streamlit? É uma biblioteca do Python que transforma os scripts de código em páginas bonitas de 
JS, HTML ou CSS sem precisar escrever de fato essas linguagens. É o front-end.

E o Make? O make é o responsável pela automação. É o que faz o agente de IA ser um agente de IA.

Custom Webhook (Gatilho): É a porta de entrada. Ele fica escutando a internet 24/7. Quando o Streamlit envia os dados da vaga, o Webhook acorda e recebe esse pacote (chamado de payload).


HTTP (Make a request): Pega o link da vaga enviado pelo Streamlit, passa para a Jina AI, e recebe de volta a descrição da vaga completamente limpa em formato de texto.

Módulo do HTTP utizamos a Jina AI para fazer uma limpeza da página, o web scraping(raspagem de dados). A Jina faz um visitinha no site e faz uma limpeza visual incrível e transforma tudo em texto, e formataado em Markdown, pra poder ser digerido fácilmente pelo Gemini AI depois.

Google Gemini AI: Recebe dois textos (a vaga limpa pela Jina + o seu currículo extraído pelo Streamlit, se tiver). O Gemini lê ambos, faz o cruzamento de dados, calcula o Match Score e redige o feedback técnico.

JSON Parse: O Gemini cospe a resposta em formato de texto estruturado. O módulo JSON Parse pega esse texto e o transforma em "pastinhas" organizadas de dados (ex: uma pasta para empresa, outra para vaga, outra para salario). É isso que permite que o Notion entenda o que é cada informação.

Router (Roteador): É um guarda de trânsito. Ele olha para a variável source que veio lá do Streamlit:

Se for streamlit_preview, ele manda o tráfego para a rota de cima.

Se for streamlit_confirmado, ele manda o tráfego para a rota de baixo.

Notion (Create a Database Item): Conectado diretamente à sua tabela do Notion. Ele recebe as pastinhas organizadas pelo JSON Parse e joga cada dado na sua respectiva coluna (Coluna Cargo, Coluna Salário, etc.).

O módulo Webhook Response é o "sedex de retorno".
Normalmente os webhook apeaans recebem os dados e depois dão tchau. Com o Response, ele consegue manter a conxeão aberta, mantendo os dados do resultado e devolvendo para o streamlit. É assim que conseguimos ver as informações da vaga antes de salva na planilha.

