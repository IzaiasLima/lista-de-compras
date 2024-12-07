def iten_html():
    html = f"""
        <h4>Cadastrar um produto</h4>

        <table class="form">
            <tr trigger="cancel" class="form editing">
                <td><input placeholder="Nome do produto" name="nome" value=""></td>
                <td>
                    <select name="categoria" required>
                        <option value="" selected hidden>Selecione</option>
                        <option value="bolachas e biscoitos">Bolachas e biscoitos</option>
                        <option value="carnes e pescado">Carnes e pescado</option>
                        <option value="doces e sobremesas">Doces e sobremesas</option>
                        <option value="enlatados">Enlatados</option>
                        <option value="farinhas e cereais">Farinhas e cereais</option>
                        <option value="farmácia">Farmácia</option>
                        <option value="frios">Frios</option>
                        <option value="horti-fruti">Horti-fruti</option>
                        <option value="higiene pessoal">Higiene pessoal</option>
                        <option value="laticínios">Laticínios</option>
                        <option value="limpeza">Limpeza</option>
                        <option value="massas">Massas</option>
                        <option value="mercearia">Mercearia</option>
                        <option value="óleos">Óleos</option>
                        <option value="produtos básicos">Produtos Básicos</option>
                        <option value="produtos naturais">Produtos naturais</option>
                        <option value="padaria">Padaria</option>
                        <option value="shopping">Shopping</option>
                        <option value="sucos e bebidas">Sucos e Bebidas</option>
                        <option value="temperos">Temperos</option>
                        <option value="utilidades">Utilidades</option>
                    </select>
                </td>
                <td><input type="hidden" name="status" value="cadastrado"></td>
            </tr>
        </table>

        <div class="icon">
            <a class="button secondary" hx-get="/api/itens"
                title="Cancelar a alteração"
                hx-swap="innerHTML" 
                hx-target="#itens">
                Cancelar
            </a>
            <a class="button primary" hx-trigger="click" 
                hx-include="table .form"
                hx-post="/api/itens" 
                title="Salvar"
                hx-swap="innerHTML" 
                hx-target="#itens">
                Salvar
            </a>
        </div>
        """
    return html
