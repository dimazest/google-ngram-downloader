from requests import Session

from google_ngram_downloader.util import get_indices
from google_ngram_downloader.__main__ import download

import pytest


@pytest.fixture
def unigram_indices():
    return set(
        '0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o other p pos '
        'punctuation q r s t u v w x y z'.split(' ')
    )


@pytest.fixture
def bigrams_indices():
    return set(
        '0 1 2 3 4 5 6 7 8 9 _ADJ_ _ADP_ _ADV_ _CONJ_ _DET_ _NOUN_ _NUM_ _PRON_ '
        '_PRT_ _VERB_ a_ aa ab ac ad ae af ag ah ai aj ak al am an ao ap aq ar '
        'as at au av aw ax ay az b_ ba bb bc bd be bf bg bh bi bj bk bl bm bn bo '
        'bp bq br bs bt bu bv bw bx by bz c_ ca cb cc cd ce cf cg ch ci cj ck cl '
        'cm cn co cp cq cr cs ct cu cv cw cx cy cz d_ da db dc dd de df dg dh di '
        'dj dk dl dm dn do dp dq dr ds dt du dv dw dx dy dz e_ ea eb ec ed ee ef '
        'eg eh ei ej ek el em en eo ep eq er es et eu ev ew ex ey ez f_ fa fb fc '
        'fd fe ff fg fh fi fj fk fl fm fn fo fp fq fr fs ft fu fv fw fx fy fz g_ '
        'ga gb gc gd ge gf gg gh gi gj gk gl gm gn go gp gq gr gs gt gu gv gw gx '
        'gy gz h_ ha hb hc hd he hf hg hh hi hj hk hl hm hn ho hp hq hr hs ht hu '
        'hv hw hx hy hz i_ ia ib ic id ie if ig ih ii ij ik il im in io ip iq ir '
        'is it iu iv iw ix iy iz j_ ja jb jc jd je jf jg jh ji jj jk jl jm jn jo '
        'jp jq jr js jt ju jv jw jx jy jz k_ ka kb kc kd ke kf kg kh ki kj kk kl '
        'km kn ko kp kq kr ks kt ku kv kw kx ky kz l_ la lb lc ld le lf lg lh li '
        'lj lk ll lm ln lo lp lq lr ls lt lu lv lw lx ly lz m_ ma mb mc md me mf '
        'mg mh mi mj mk ml mm mn mo mp mq mr ms mt mu mv mw mx my mz n_ na nb nc '
        'nd ne nf ng nh ni nj nk nl nm nn no np nq nr ns nt nu nv nw nx ny nz o_ '
        'oa ob oc od oe of og oh oi oj ok ol om on oo op oq or os ot other ou ov '
        'ow ox oy oz p_ pa pb pc pd pe pf pg ph pi pj pk pl pm pn po pp pq pr ps '
        'pt pu punctuation pv pw px py pz q_ qa qb qc qd qe qf qg qh qi qj qk ql '
        'qm qn qo qp qq qr qs qt qu qv qw qx qy qz r_ ra rb rc rd re rf rg rh ri '
        'rj rk rl rm rn ro rp rq rr rs rt ru rv rw rx ry rz s_ sa sb sc sd se sf '
        'sg sh si sj sk sl sm sn so sp sq sr ss st su sv sw sx sy sz t_ ta tb tc '
        'td te tf tg th ti tj tk tl tm tn to tp tq tr ts tt tu tv tw tx ty tz u_ '
        'ua ub uc ud ue uf ug uh ui uj uk ul um un uo up uq ur us ut uu uv uw ux '
        'uy uz v_ va vb vc vd ve vf vg vh vi vj vk vl vm vn vo vp vq vr vs vt vu '
        'vv vw vx vy vz w_ wa wb wc wd we wf wg wh wi wj wk wl wm wn wo wp wq wr '
        'ws wt wu wv ww wx wy wz x_ xa xb xc xd xe xf xg xh xi xj xk xl xm xn xo '
        'xp xq xr xs xt xu xv xw xx xy xz y_ ya yb yc yd ye yf yg yh yi yj yk yl '
        'ym yn yo yp yq yr ys yt yu yv yw yx yy yz z_ za zb zc zd ze zf zg zh zi '
        'zj zk zl zm zn zo zp zq zr zs zt zu zv zw zx zy zz'.split(' ')
    )


def test_get_indices_1grams(unigram_indices):
    indices = list(get_indices(1))
    assert len(set(indices)) == len(indices)

    assert set(indices) == unigram_indices


def test_get_indices_manygrams(bigrams_indices):
    indices = list(get_indices(2))
    assert len(set(indices)) == len(indices)

    assert set(indices) == bigrams_indices


@pytest.mark.parametrize(
    ('verbose', 'err_len'),
    (
        (False, 1),
        (True, 725),
    ),
)
def test_download(capsys, tmpdir, monkeypatch, verbose, err_len):
    urls = []

    def mocked_get(self, url, **kwargs):
        urls.append(url)

        class FakeRequest:

            def iter_content(self, buffer):
                yield b'some data'

        return FakeRequest()

    monkeypatch.setattr(Session, 'get', mocked_get)

    download.command(
        '-o {tmpdir} -n 2 {verbose}'
        ''.format(
            tmpdir=tmpdir,
            verbose='-v' if verbose else '',
        ).split()
    )

    assert len(urls) == len(tmpdir.listdir()) == 724

    out, err = capsys.readouterr()
    assert not out
    assert len(err.split('\n')) == err_len
