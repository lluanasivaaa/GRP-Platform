# 🔐 Política de Segurança

## Relatando Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança, por favor **NÃO** abra uma Issue pública. Em vez disso:

1. **Envie um email** para: lluanasivaaa@gmail.com
2. **Descreva** a vulnerabilidade com detalhes
3. **Forneça** passos para reproduzir (se possível)
4. **Aguarde** resposta dentro de 48 horas

Informações sobre a vulnerabilidade serão mantidas em sigilo até que uma correção seja lançada.

## Recomendações de Segurança

### Para Desenvolvimento

```python
# ✅ BOM - Prepared statements
cursor.execute("SELECT * FROM riscos WHERE id_risco = %s", (id,))

# ❌ RUIM - SQL Injection vulnerability
query = f"SELECT * FROM riscos WHERE id_risco = {id}"
cursor.execute(query)
```

```python
# ✅ BOM - Validação de entrada
def validar_email(email):
    import re
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("Email inválido")
    return email

# ❌ RUIM - Sem validação
def usar_email(email):
    return email
```

### Para Produção

1. **Autenticação**
   - Implemente autenticação forte (OAuth 2.0)
   - Use hash seguro para senhas (bcrypt, argon2)
   - Implemente 2FA

2. **Dados Sensíveis**
   - Criptografe dados em trânsito (HTTPS/TLS)
   - Criptografe dados em repouso
   - Use variáveis de ambiente para credenciais
   - Nunca commite `.env` ou `secrets.json`

3. **Banco de Dados**
   - Limite permissões de usuário
   - Use conexões encriptadas
   - Fazer backups regulares e testados
   - Implementar retenção de logs de auditoria

4. **Aplicação**
   - Validar e sanitizar todas as entradas
   - Implementar rate limiting
   - CORS configurado corretamente
   - Logs de segurança e auditoria
   - Testes de segurança regulares

5. **Infraestrutura**
   - Firewall configurado
   - HTTPS obrigatório
   - Atualizações de segurança aplicadas
   - Monitoramento e alertas

## Práticas de Código Seguro

### Prevenção de SQL Injection
```python
# Use parametrized queries
db.execute("INSERT INTO projetos (nome, responsavel) VALUES (?, ?)", 
           (nome, responsavel))
```

### Validação de Entrada
```python
def validar_entrada(valor, tipo, tamanho_maximo=255):
    if not isinstance(valor, tipo):
        raise TypeError(f"Esperado {tipo}, recebido {type(valor)}")
    if len(str(valor)) > tamanho_maximo:
        raise ValueError("Valor excede tamanho máximo")
    return valor
```

### Proteção de Credenciais
```python
# .env (nunca commitar!)
DB_PASSWORD=minha_senha_secreta

# Uso seguro
import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv('DB_PASSWORD')
```

## Dependências de Segurança

Mantenha dependências atualizadas:

```bash
# Verificar vulnerabilidades conhecidas
pip install safety
safety check

# Atualizar dependências
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

## Testes de Segurança

Considere usar ferramentas de análise de segurança:

- **Bandit**: Detecta problemas de segurança em código Python
- **Safety**: Verifica dependências contra database de vulnerabilidades
- **OWASP ZAP**: Testes de segurança de aplicações web

```bash
# Exemplo: Bandit
pip install bandit
bandit -r risk_management_system/
```

## Divulgação Responsável

Seguimos práticas de divulgação responsável:

1. **Reporte** enviado para contato de segurança
2. **Confirmação** dentro de 48 horas
3. **Investigação** e desenvolvimento de correção
4. **Lançamento** de patch de segurança
5. **Divulgação** pública após patch disponível

## Histórico de Segurança

| Data | Vulnerability | Status |
|------|---------------|--------|
| N/A | N/A | Nenhuma reportada até agora |

## Links Úteis

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Secure Coding](https://cheatsheetseries.owasp.org/)
- [Python Security](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)

---

**Última Atualização:** 02 de Junho de 2026

Obrigada por ajudar a manter este projeto seguro! 🛡️
