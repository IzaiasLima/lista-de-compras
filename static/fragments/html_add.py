def item_html():
    html = f"""
        <h4>Cadastrar um produto</h4>

        <table class="form">
            <tr trigger="cancel" class="form editing">
                <td><input placeholder="Nome do produto" name="nome" value=""></td>
                <td>
                    <select name="categoria">
                        <option value="" selected disabled hidden>Selecione</option>
                        <option value="carnes e peixes">Carnes e Peixes</option>
                        <option value="enlatados">Enlatados</option>
                        <option value="frios">Frios</option>
                        <option value="hortifrutigranjeiros">Hortifrutigranjeiros</option>
                        <option value="laticínios">Laticínios</option>
                        <option value="produtos básicos">Produtos Básicos</option>
                        <option value="produtos de limpeza">Produtos de Limpeza</option>
                        <option value="sucos e bebidas">Sucos e Bebidas</option>
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