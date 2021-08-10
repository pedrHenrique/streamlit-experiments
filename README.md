# automacao-sst-e2e

## Baixando e Instalando o Projeto

1. Clone o repositório
```
git clone gitlab.contmatic.com.br/thiago.graca/automacao-sst-e2e.git
```
2. Instale as dependências do projeto
```
npm install
```
Caso você não possua o NPM, você pode obter ele clicando neste [**Link**](https://nodejs.org/pt-br/)

3. Insira seu usuário no arquivo de constantes sempre que for executar seus testes
```
login_default = 'seuusuario@sstgestao'
```
> Caminho para arquivo de constantes cypress/util/constants/constants.js

4. Inicie o Cypress
```
npm run cypress:open
```

**Pronto, você já vai estar pronto para começar a criar e executar seus testes.**

## Arquivos e Diretórios do Projeto

O projeto não possui a maior quantidade de arquivos e diretórios, porém possui o suficiente para nós confundir algumas vezes.<br>
Aqui vai um resumo de cada diretório/arquivo e sua respectiva função atualmente.

### Diretórios

* cypress/plugins & cypress/support

Diretório de configurações auxiliares.<br>
Nestes diretórios se encontram desde configurações sobres os cookies, plugins, comandos adicionais, até mesmo os comandos executados antes/depois dos cenários/steps.

* cypress/integration

Diretório dos testes.<br>
E nele onde críamos nossos casos de testes que serão executados no sistema.

* cypress/util/PageObject

Diretório para mapeamentos dos elementos.<br>
Aqui se encontram todos os mapeamentos dos elementos utilizados nos testes, desde botões, popups, campos de texto e etc.<br>

* cypress/util/pages

Diretório para criação de métodos auxiliares que são chamados constantemente nos arquivos de testes.<br>
Aqui é um ótimo lugar para criar métodos que validam ou fazem algo específico, que só o caso de teste que você estiver escrevendo use.

***Todo novo caso de teste que for iniciado, deve obrigatoriamente possuir um arquivo na _PageObject_ com seus mapeamentos,<br>
como também um arquivo na _page_ com os métodos que seu caso de teste irá utilizar.***

### Arquivos

* Base.js

Arquivo base para grande maioria das ações e validações mais comuns que utilizamos nos testes com o cypress.<br>
Nele há diversos métodos auxiliares, que normalmente podem ser executados em diversos elementos do sistema inteiro,
apenas fornecendo o elemento no qual o cypress deve interagir.

**Exemplo**
```
base.preencher(profissionalMap.nome_completo, constants.MaisSessentaCaracteres)
```

Nem sempre a base terá a melhor validação para um cenário de um teste específico. 
Mas pelo menos já consegue encapsular grande parte das ações mais comums que alguns cenários pedem.

* constants.js

Arquivo de constantes.<br>
Muito útil para referenciar textos com 60+ caracteres, como também para definir variáveis que outros testes podem usar.

* cypress.json

_TODO_
