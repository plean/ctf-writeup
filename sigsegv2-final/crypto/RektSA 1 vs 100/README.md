# Sigsegv2 final

## Crypto

### RektSA 1 vs 100

Writeup par plean

Ce challenge est dans la continuation du RektSA, challenge de crypto des qualifications.
En plus de demander a ce qu'on retrouve $d$, ce challenge demandais a ce que l'on retrouve aussi $p$ et $q$.

La partie permetant de trouver $phi$ puis $d$ ayant deja ete explique dans plusieurs writeup je ne la reexpliquerai pas, [celui-ci](https://rtfm.re/writeups/Shutdown.html) par exemple utilise la meme methode que moi pour trouver $d$.

----------

Une fois que $phi$ est trouve on peut en deduire $p$ et $q$.

Comme nous connaissons $r$ nous pouvons simplifier le probleme on factorisant $N/r$. 
Pour ce faire nous utiliserons la [definition](https://fr.wikipedia.org/wiki/Indicatrice_d'Euler#Calcul) de l'indicatrice d'Euler:

$$\varphi{(n)} = (p - 1)(q - 1) = pq - p - q + 1 = (n + 1) - (p + q)$$

Nous pouvons donc ecrire:

$$(n + 1) - \varphi{(n)} = p + q$$
$$(n + 1) - \varphi{(n)} - p = q$$

Nous savons d'apres [RSA](https://fr.wikipedia.org/wiki/Chiffrement_RSA#Cr%C3%A9ation_des_cl%C3%A9s) que:

$$n = pq$$

En ramplacant $q$ par $(n+1)−φ(n)−p$ nous pouvons en deduire que:

$$n = p \left ( n + 1 - \varphi{(n)} - p \right ) = -p^2 + (n + 1 - \varphi{(n)})p$$

En rearrangeant un peu on trouve:

$$p^2 - (n + 1 - \varphi{(n)})p + n = 0$$

Ceci est une équation quadratique en $p$, avec:

$$a = 1 \\ b = -(n + 1 - \varphi{(n)}) \\ c = n $$

Ce qui peut être facilement résolu en utilisant la formule quadratique:


$$p = \frac{-b \pm \sqrt{|b|^2 - 4ac}}{2a} = \frac{(n + 1 - \varphi{(n)}) \pm \sqrt{|n + 1 - \varphi{(n)}|^2 - 4n}}{2}$$

Les deux solutions pour $p$ seront les facteurs premier de $n$, $p$ et $q$.

----------

Une fois implemente notre code ressemblera a ca:
```python
	gmpy2.get_context().precision=2048
	pq_phi = phi // (r-1)
	Nmr = N // r

	a = 1
        b = -(Nmr + 1 - pq_phi)
        c = Nmr

        x = gmpy2.sqrt(gmpy2.mpz(b**2 - 4 * c))
        p = int((-b + x) / 2)
	q = int((-b - x) / 2)
```

Il nous reste a verifier nos solutions

```python
            assert q * p * r == N
            assert (q-1) * (p-1) * (r-1) == phi
```
On lance notre script et on recupere le flag :)
```bash
$ python3 solv.py
[+] Opening connection to finale-challs.rtfm.re on port 9002: Done
Congratulations: sigsegv{s0_y0u_c4n_s0lv3_1t_w1th_r_4ft3r_4ll...}
[*] Closed connection to finale-challs.rtfm.re port 9002
```

