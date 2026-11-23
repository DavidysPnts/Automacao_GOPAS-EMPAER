import math
from src.config import RAIO_TOLERANCIA_METROS


def calcular_distancia_metros(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula a distância geodésica em metros entre dois pontos (fórmula de Haversine)."""
    # Raio médio da Terra em metros (6.371 km)
    raio_terra_m = 6_371_000.0

    # Converte as latitudes de graus decimais para radianos (exigido por math.sin e math.cos)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)

    # Calcula a variação (delta) de latitude e longitude entre os dois pontos em radianos
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    # Equação de Haversine: calcula o quadrado da metade do comprimento da corda entre os pontos na esfera
    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )

    # Converte o valor 'a' no ângulo central (via arco-tangente) e multiplica pelo raio da Terra para obter metros
    return 2 * raio_terra_m * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def auditar_geolocalizacao(
    coord_propriedade: tuple[float, float] | None,
    coord_atendimento: tuple[float, float] | None,
    raio_tolerancia: float = RAIO_TOLERANCIA_METROS,
) -> list[str]:
    """
    Compara as coordenadas da propriedade cadastrada com as do atendimento.
    Só dispara validação se o beneficiário possuir propriedade cadastrada.
    """
    if not coord_propriedade:
        return []  # Beneficiário sem propriedade cadastrada; regra não se aplica

    if not coord_atendimento:
        return ["Beneficiário possui propriedade cadastrada, mas atendimento está sem coordenadas"]

    distancia = calcular_distancia_metros(
        coord_propriedade[0], coord_propriedade[1],
        coord_atendimento[0], coord_atendimento[1],
    )

    if distancia > raio_tolerancia:
        return [
            f"Divergência de geolocalização: {distancia:.0f}m da propriedade "
            f"(limite: {raio_tolerancia:.0f}m)"
        ]

    return []