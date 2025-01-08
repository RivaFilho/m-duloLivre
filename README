# Snake Game - Estrutura e Funcionamento

Este documento explica o funcionamento do código, descreve as classes, suas responsabilidades, e como conceitos de programação orientada a objetos, como encapsulamento, herança e polimorfismo, são aplicados.

## Estrutura do Código

O código é uma implementação do clássico jogo da cobrinha (Snake) utilizando a biblioteca `pygame`. Ele é dividido em várias classes para organização e reutilização de código:

### Classes

#### 1. `GameObject`
- **Descrição**: Classe base para representar objetos no jogo.
- **Responsabilidades**:
  - Armazena as coordenadas `x` e `y` do objeto.
  - Define o método abstrato `render` que deve ser implementado pelas classes filhas.
- **Conceitos Aplicados**:
  - **Herança**: Outras classes, como `Snake` e `Food`, herdam de `GameObject`.
  - **Polimorfismo**: Cada classe filha implementa o método `render` de forma diferente.

#### 2. `Snake`
- **Descrição**: Representa a cobra do jogo.
- **Responsabilidades**:
  - Controla o corpo da cobra, direção e movimentos.
  - Gerencia o crescimento e encurtamento do corpo da cobra.
  - Desenha a cobra na tela.
- **Relação com Outras Classes**: Herda de `GameObject`.
- **Conceitos Aplicados**:
  - **Encapsulamento**: O estado da cobra (como posição e direção) é mantido dentro da classe.
  - **Polimorfismo**: Implementa o método `render` para desenhar cada segmento do corpo.

#### 3. `Food`
- **Descrição**: Representa a comida que a cobra deve coletar.
- **Responsabilidades**:
  - Gerar uma posição aleatória na tela.
  - Desenhar a comida na tela.
- **Relação com Outras Classes**: Herda de `GameObject`.
- **Conceitos Aplicados**:
  - **Encapsulamento**: A posição da comida é mantida dentro da classe.
  - **Polimorfismo**: Implementa o método `render` para desenhar a comida.

#### 4. `Player`
- **Descrição**: Representa o jogador e gerencia o registro de pontuações.
- **Responsabilidades**:
  - Carregar e salvar pontuações em um arquivo JSON.
  - Atualizar pontuações baseadas na dificuldade.
  - Fornecer acesso às pontuações do jogador.
- **Relação com Outras Classes**: Utilizada pelo `Game` para armazenar e consultar pontuações.
- **Conceitos Aplicados**:
  - **Encapsulamento**: As pontuações e o nome do jogador são mantidos privados dentro da classe.

#### 5. `Game`
- **Descrição**: Controla o fluxo geral do jogo.
- **Responsabilidades**:
  - Gerencia o estado do jogo, como inicialização, execução e término.
  - Implementa as telas principais, como registro de usuário, seleção de dificuldade e "Game Over".
  - Interage com as outras classes (`Snake`, `Food`, `Player`) para criar a lógica do jogo.
- **Relação com Outras Classes**: Centraliza a interação entre todas as classes.
- **Conceitos Aplicados**:
  - **Encapsulamento**: Gerencia o estado geral do jogo, como a dificuldade e a pontuação.

## Funcionamento Geral

### Registro do Jogador
- O jogo começa com uma tela para registrar o nome do jogador.
- A entrada é armazenada na classe `Player`, que gerencia as pontuações associadas ao jogador.

### Seleção de Dificuldade
- Após o registro, uma tela permite ao jogador selecionar a dificuldade: `Fácil`, `Médio`, `Difícil` ou `Impossível`.
- A dificuldade selecionada ajusta a velocidade da cobra.

### Execução do Jogo
- O jogo principal ocorre em um loop controlado pela classe `Game`.
- A cobra (`Snake`) se move pela tela e coleta comida (`Food`).
- A pontuação é incrementada a cada coleta e exibida no canto superior esquerdo.

### Tela de "Game Over"
- Quando a cobra colide consigo mesma ou com as bordas da tela, o jogo termina.
- O jogador pode escolher entre:
  - **Retry**: Reiniciar o jogo.
  - **Logout**: Retornar à tela de registro de usuário.
  - **Exit**: Encerrar o programa.
  - **Scores**: Ver as pontuações do jogador em todas as dificuldades.
  - **Change Difficulty**: Retornar à tela de seleção de dificuldade.

## Uso dos Conceitos de POO

### Encapsulamento
- Cada classe mantém seus próprios dados e métodos para manipulá-los.
- Exemplo: A posição da cobra e seu movimento são encapsulados na classe `Snake`.

### Herança
- `Snake` e `Food` herdam de `GameObject` para reutilizar código comum, como as coordenadas `x` e `y`.

### Polimorfismo
- O método `render` é redefinido em `Snake` e `Food` para desenhar objetos específicos na tela.

## Arquivo JSON para Pontuações
- As pontuações são salvas em um arquivo `players.json` no seguinte formato:
```json
{
    "jogador1": {
        "scores": {
            "Fácil": 10,
            "Médio": 25,
            "Difícil": 40,
            "Impossível": 60
        }
    }
}
```

- A classe `Player` é responsável por carregar e salvar essas informações.

## Como Jogar
1. Registre um nome de usuário.
2. Selecione uma dificuldade.
3. Controle a cobra com as teclas:
   - **W/Seta para cima**: Subir.
   - **A/Seta para esquerda**: Esquerda.
   - **S/Seta para baixo**: Descer.
   - **D/Seta para direita**: Direita.
4. Colete a comida e aumente sua pontuação.
5. Se o jogo terminar, escolha entre as opções da tela de "Game Over".

---
Este código demonstra uma implementação estruturada e reutilizável do jogo da cobrinha, utilizando princípios fundamentais de programação orientada a objetos.

