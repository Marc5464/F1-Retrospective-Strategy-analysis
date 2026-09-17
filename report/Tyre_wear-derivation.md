Assuming tyre wear is linear (with respect to trye age $a_l$ ) within the 25 lap cap:

$$
\Delta t_{\text{wear}}(a_l, \text{tyre}) = K_{\text{tyre}} + m_{\text{tyre}} \cdot a_l
$$

So for a stint of length $N = \|\text{stint}\|$, the total accumulated tire wear penalty simplifies to:

$$
\sum_{l=1}^{N} \Big( K_{\text{tyre}} + m_{\text{tyre}} \cdot l \Big) = K_{\text{tyre}} \cdot N + \frac{m_{\text{tyre}}}{2} \cdot N (N + 1)
$$

<table>
  <tr valign="top">
    <td width="50%">

* **$K_{\text{tyre}}$**: Base performance offset for the compound relative to baseline (e.g., $K_{\text{medium}} < K_{\text{hard}}$).
* **$m_{\text{tyre}}$**: Linear degradation slope per lap of age ($\text{s}/\text{lap}^2$).

    </td>
    <td width="50%">

* **$N$**: Total lap length of the stint ($N = \|\text{stint}\|$).
* **$a_l$**: Age of the tire on lap $l$ ($a_l \in [1, N]$).

    </td>
  </tr>
</table>

* **$T_1$ Strategy (Variable 3-Stint Strategy):**
  * Stint lengths: $S_1, S_2, S_3$
  * Conservation constraint: $S_1 + S_2 + S_3 = 57$
  * Compound usage: $S_1$ (Medium), $S_2$ (Medium), $S_3$ (Hard)

* **$T_2$ Strategy (Fixed 3-Stint Strategy via Lap 7 Safety Car Pit Stop):**
  * Stint lengths: $S_{2,1} = 7$, $S_{2,2} = 25$, $S_{2,3} = 25$ ($7 + 25 + 25 = 57$)
  * Compound usage: $S_{2,1}$ (Medium), $S_{2,2}$ (Medium), $S_{2,3}$ (Hard)

Using our linear summation formula for both times:

$$
T_{1, \text{wear}} = \left[ K_{\text{M}} S_1 + \frac{m_{\text{M}}}{2} S_1(S_1 + 1) \right] + \left[ K_{\text{M}} S_2 + \frac{m_{\text{M}}}{2} S_2(S_2 + 1) \right] + \left[ K_{\text{H}} S_3 + \frac{m_{\text{H}}}{2} S_3(S_3 + 1) \right]
$$

Group:

$$
T_{1, \text{wear}} = K_{\text{M}}(S_1 + S_2) + K_{\text{H}} S_3 + \frac{m_{\text{M}}}{2}\Big[ S_1(S_1 + 1) + S_2(S_2 + 1) \Big] + \frac{m_{\text{H}}}{2}\Big[ S_3(S_3 + 1) \Big]
$$

Now for $T_2$

By substituting fixed stint lengths $S_{2,1} = 7$, $S_{2,2} = 25$, and $S_{2,3} = 25$:

$$
T_{2, \text{wear}} = \left[ 7 K_{\text{M}} + \frac{m_{\text{M}}}{2} (7)(8) \right] + \left[ 25 K_{\text{M}} + \frac{m_{\text{M}}}{2} (25)(26) \right] + \left[ 25 K_{\text{H}} + \frac{m_{\text{H}}}{2} (25)(26) \right]
$$

simplifying 

$$
T_{2, \text{wear}} = 32 K_{\text{M}} + 25 K_{\text{H}} + 353 m_{\text{M}} + 325 m_{\text{H}}
$$


Now take the difference of the constant $K_{\text{tyre}}$

$$
K_{\text{M}}(S_1 + S_2 - 32) + K_{\text{H}}(S_3 - 25)
$$

Since $S_3 = 57 - S_1 - S_2$, we substituting for $S_3$:

$$
K_{\text{H}}(57 - S_1 - S_2 - 25) = K_{\text{H}}(32 - S_1 - S_2) = -K_{\text{H}}(S_1 + S_2 - 32)
$$

Factoring out $(S_1 + S_2 - 32)$:

$$
(K_{\text{M}} - K_{\text{H}})(S_1 + S_2 - 32)
$$

Now simplifying the slopes $m$

$$
\frac{m_{\text{M}}}{2} \Big[ S_1(S_1 + 1) + S_2(S_2 + 1) - (56 + 650) \Big] = \frac{m_{\text{M}}}{2} \Big[ S_1(S_1 + 1) + S_2(S_2 + 1) - 706 \Big]
$$


$$
\frac{m_{\text{H}}}{2} \Big[ S_3(S_3 + 1) - 650 \Big]
$$

Combine

$$
\Delta T_{\text{wear}} = (K_{\text{M}} - K_{\text{H}})(S_1 + S_2 - 32) + \frac{m_{\text{M}}}{2} \Big[ S_1(S_1 + 1) + S_2(S_2 + 1) - 706 \Big] + \frac{m_{\text{H}}}{2} \Big[ S_3(S_3 + 1) - 650 \Big]
$$

<table>
  <tr valign="top">
    <td width="50%">

* **$S_1, S_2, S_3$**: Stint lengths for $T_1$ ($S_1 + S_2 + S_3 = 57$ and $S_i \le 25$).
* **$K_{\text{M}}, K_{\text{H}}$**: Compound base pace offset relative to baseline ($s$).
* **$m_{\text{M}}, m_{\text{H}}$**: Linear tire degradation slope ($\text{s}/\text{lap}^2$).

    </td>
    <td width="50%">

* **$7, 25, 25$**: Fixed stint lengths for $T_2$ (pitting on Laps 7 and 32 under the SC strategy).
* **$706, 650$**: Closed-form constants evaluating $T_2$'s quadratic series ($7 \times 8 + 25 \times 26 = 706$ and $25 \times 26 = 650$).

    </td>
  </tr>
</table>
