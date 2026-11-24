"""Calculadora financeira (break-even) - Fase D.

Puro, sem I/O, sem dependencias externas: usado pelo endpoint web
(/api/finance/calc em app_core.py) e, no futuro, pelo Gestor de Trafego IA
para citar numeros reais de break-even de uma oferta.
"""


def calc_breakeven(price, gateway_fee_pct=0.0, gateway_fee_fixed=0.0,
                    other_costs=0.0, target_margin_pct=0.0,
                    ad_spend=None, purchases=None):
    """Calcula quanto sobra por venda e o quanto se pode pagar em anuncio.

    price: preco de venda do produto (obrigatorio, > 0).
    gateway_fee_pct: taxa percentual da plataforma de pagamento (ex.: 9.9).
    gateway_fee_fixed: taxa fixa por venda da plataforma (ex.: R$1,00).
    other_costs: outros custos por venda (producao, comissao de afiliado...).
    target_margin_pct: margem de lucro desejada sobre o preco de venda.
    ad_spend / purchases: opcionais, para estimar o lucro liquido real de
    um periodo ja rodado.

    Retorna: net_price_per_sale, max_cpa, breakeven_roas, net_profit (ou
    None quando ad_spend/purchases nao foram informados).
    """
    if price is None or price <= 0:
        raise ValueError("price deve ser maior que zero")
    gateway_fee_pct = max(0.0, gateway_fee_pct or 0.0)
    gateway_fee_fixed = max(0.0, gateway_fee_fixed or 0.0)
    other_costs = max(0.0, other_costs or 0.0)
    target_margin_pct = max(0.0, target_margin_pct or 0.0)

    net_price_per_sale = (
        price
        - (price * gateway_fee_pct / 100.0)
        - gateway_fee_fixed
        - other_costs
    )
    desired_profit_per_sale = price * target_margin_pct / 100.0
    max_cpa = net_price_per_sale - desired_profit_per_sale
    breakeven_roas = (price / net_price_per_sale) if net_price_per_sale > 0 else None

    net_profit = None
    if ad_spend is not None and purchases is not None:
        net_profit = (purchases * net_price_per_sale) - ad_spend

    return {
        "net_price_per_sale": round(net_price_per_sale, 2),
        "max_cpa": round(max_cpa, 2),
        "breakeven_roas": round(breakeven_roas, 2) if breakeven_roas is not None else None,
        "net_profit": round(net_profit, 2) if net_profit is not None else None,
    }
