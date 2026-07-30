"""
Gera os STLs das 3 peças do carrinho porta-cabos VAHLE WS1F85-50-90-K.
Arquitetura v9: 1 travessa em cruz + 2 corpos de roldana idênticos.

ATENÇÃO: as cotas abaixo ainda são ESTIMATIVAS (ver folha_de_medicao.md).
Só o Ø/largura da roldana e o envelope do catálogo estão confirmados.
"""
import numpy as np, struct, sys
from skimage import measure

# ---------------- cotas (as mesmas do visualizador 3D) ----------------
# roldana — MEDIDO
roda_De, roda_Dg, roda_larg = 35.0, 20.0, 16.0
# corpo — ESTIMADO
corpo_H, corpo_Wt, corpo_Wb, corpo_E = 52.0, 42.0, 24.0, 26.0
roda_Y, fenda_W = 34.0, 13.0
furo_eixo = 8.5
# travessa — ESTIMADO (A e B vêm do catálogo)
trav_L, trav_B, trav_W, trav_H = 90.0, 55.0, 22.0, 14.0
sep, furo_1, furo_2, furo_D, garfo_H = 71.0, 14.0, 22.0, 7.0, 18.0
# impressão
par = 3.5          # parede mínima
folga_pino = 0.4   # folga do furo do pino
RES = float(sys.argv[1]) if len(sys.argv) > 1 else 0.4


# ---------------- utilitários de SDF ----------------
def grid(x0, x1, y0, y1, z0, z1, r=RES):
    x = np.arange(x0, x1 + r, r, dtype=np.float32)
    y = np.arange(y0, y1 + r, r, dtype=np.float32)
    z = np.arange(z0, z1 + r, r, dtype=np.float32)
    return np.meshgrid(x, y, z, indexing="ij"), (x[0], y[0], z[0])


def rbox(X, Y, cx, cy, hx, hy, r=0.0):
    dx = np.abs(X - cx) - (hx - r)
    dy = np.abs(Y - cy) - (hy - r)
    return (np.sqrt(np.maximum(dx, 0) ** 2 + np.maximum(dy, 0) ** 2)
            + np.minimum(np.maximum(dx, dy), 0) - r)


def slab(A, a0, a1):
    return np.maximum(a0 - A, A - a1)


def cyl(A, B, ca, cb, r):
    return np.sqrt((A - ca) ** 2 + (B - cb) ** 2) - r


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def salva(d, org, nome):
    v, f, _, _ = measure.marching_cubes(d, level=0.0, spacing=(RES, RES, RES))
    v = v + np.array(org, dtype=np.float32)
    tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    raw = np.zeros(len(f), dtype=[("d", "<f4", 12), ("a", "<u2")])
    raw["d"][:, 0:3] = n
    raw["d"][:, 3:12] = tri.reshape(-1, 9)
    with open(nome, "wb") as fh:
        fh.write(b"\0" * 80)
        fh.write(struct.pack("<I", len(f)))
        fh.write(raw.tobytes())
    vol = float((d < 0).sum()) * RES ** 3 / 1000.0
    bb = v.max(0) - v.min(0)
    print(f"{nome:34s} {len(f):7d} tri  "
          f"{bb[0]:5.1f} x {bb[1]:5.1f} x {bb[2]:5.1f} mm  "
          f"{vol:5.1f} cm3  ~{vol*1.27*0.45:4.1f} g (PETG, 45%)")
    return vol


# ==================== PEÇA 1 — CORPO DA ROLDANA ====================
def corpo():
    Hb = garfo_H + 4                      # garfo desce abaixo do pino
    (X, Y, Z), org = grid(-corpo_Wt/2-3, corpo_Wt/2+3, -Hb-3, corpo_H+3,
                          -corpo_E/2-3, corpo_E/2+3)

    # silhueta: trapézio que abre da base para o topo, topo arredondado
    tronco = rbox(X, Y, 0, corpo_H*0.5, corpo_Wb/2, corpo_H*0.5, 2.0)
    topo   = rbox(X, Y, 0, corpo_H-14, corpo_Wt/2, 14.0, 10.0)
    perfil = smin(tronco, topo, 9.0)
    solido = np.maximum(perfil, slab(Z, -corpo_E/2, corpo_E/2))

    # garfo inferior: duas orelhas que abraçam a travessa
    orelha = np.maximum(rbox(X, Y, 0, -Hb/2, corpo_Wb/2, Hb/2, 3.0),
                        slab(Z, -corpo_E/2, corpo_E/2))
    solido = smin(solido, orelha, 5.0)

    # bolso da roldana: rasgo passante na espessura + folga radial
    bolso = np.maximum(cyl(X, Y, 0, roda_Y, (roda_De + 1.5) / 2),
                       slab(Z, -(roda_larg + 1) / 2, (roda_larg + 1) / 2))
    # fenda do cabo: sobe do bolso até o topo, aberta
    fenda = np.maximum(np.maximum(np.abs(Z) - fenda_W / 2, slab(Y, roda_Y, corpo_H + 5)),
                       np.abs(X) - (roda_De + 1.5) / 2)
    # vão do garfo: abre entre as orelhas para entrar a travessa
    vao = np.maximum(np.maximum(np.abs(Z) - (trav_W + 1.2) / 2, slab(Y, -Hb - 5, 2.0)),
                     np.abs(X) - corpo_Wb / 2 - 1)

    furos = np.minimum(
        np.maximum(cyl(X, Y, 0, roda_Y, (furo_eixo + folga_pino) / 2), slab(Z, -50, 50)),
        np.maximum(cyl(X, Y, 0, -garfo_H / 2, (furo_D + folga_pino) / 2), slab(Z, -50, 50)))

    d = np.maximum(solido, -np.minimum.reduce([bolso, fenda, vao, furos]))
    return d, org


# ==================== PEÇA 2 — TRAVESSA EM CRUZ ====================
def travessa():
    Ht = trav_H + garfo_H + 4
    (X, Y, Z), org = grid(-trav_L/2-3, trav_L/2+3, -trav_H/2-3, trav_H/2+garfo_H+5,
                          -trav_B/2-3, trav_B/2+3)

    braco_x = np.maximum(rbox(X, Z, 0, 0, trav_L/2, trav_W/2, 5.0),
                         slab(Y, -trav_H/2, trav_H/2))
    braco_z = np.maximum(rbox(X, Z, 0, 0, trav_W/2, trav_B/2, 5.0),
                         slab(Y, -trav_H/2, trav_H/2))
    solido = np.minimum(braco_x, braco_z)

    # orelhas da articulação nas pontas do braço longo
    for s in (-1, 1):
        for zz in (-1, 1):
            o = np.maximum(rbox(X, Z, s*sep/2, zz*(trav_W/2 - 2.5), 7.0, 2.5, 1.5),
                           slab(Y, trav_H/2 - 2, trav_H/2 + garfo_H))
            solido = smin(solido, o, 3.0)

    # alívio interno: vira perfil C, aberto por cima
    alivio = np.minimum(
        np.maximum(rbox(X, Z, 0, 0, trav_L/2 - par, trav_W/2 - par, 3.0),
                   slab(Y, -trav_H/2 + par, trav_H/2 + 5)),
        np.maximum(rbox(X, Z, 0, 0, trav_W/2 - par, trav_B/2 - par, 3.0),
                   slab(Y, -trav_H/2 + par, trav_H/2 + 5)))
    # não deixa o alívio comer a raiz das orelhas
    for s in (-1, 1):
        macico = np.maximum(rbox(X, Z, s*sep/2, 0, 8.0, trav_W/2, 2.0),
                            slab(Y, -50, 50))
        alivio = np.maximum(alivio, -macico)

    furos = None
    for s in (-1, 1):
        for d0 in (furo_1, furo_2):
            f = np.maximum(cyl(X, Z, 0, s*d0, furo_D/2), slab(Y, -50, 50))
            furos = f if furos is None else np.minimum(furos, f)
        # furo do pino da articulação, atravessa as duas orelhas
        fp = np.maximum(cyl(X, Y, s*sep/2, trav_H/2 + garfo_H - 6, (furo_D + folga_pino)/2),
                        slab(Z, -50, 50))
        furos = np.minimum(furos, fp)

    d = np.maximum(solido, -np.minimum(alivio, furos))
    return d, org


if __name__ == "__main__":
    print(f"resolução da malha: {RES} mm\n")
    v1 = salva(*corpo(), "corpo_roldana_ESTIMATIVA_v1.stl")
    v2 = salva(*travessa(), "travessa_cruz_ESTIMATIVA_v1.stl")
    print(f"\nconjunto (2 corpos + 1 travessa): {2*v1+v2:.1f} cm3, "
          f"~{(2*v1+v2)*1.27*0.45:.0f} g em PETG a 45% de preenchimento")
    print("ficha do fabricante: conjunto K original pesa 130 g")
