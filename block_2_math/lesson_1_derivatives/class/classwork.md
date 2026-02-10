# Производная функции

## 1. Определение производной

**Производной функции** $f(x)$ в точке $x_0$ называется предел:

$$f'(x_0) = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x}$$

Альтернативная запись:

$$f'(x_0) = \lim_{h \to 0} \frac{f(x_0 + h) - f(x_0)}{h}$$

**Геометрический смысл:** производная равна тангенсу угла наклона касательной к графику функции в данной точке.

**Физический смысл:** производная пути по времени — это скорость; производная скорости по времени — это ускорение.

---

## 2. Правила дифференцирования

### 2.1. Линейность

$$(C \cdot f(x))' = C \cdot f'(x)$$

$$(f(x) + g(x))' = f'(x) + g'(x)$$

### 2.2. Производная произведения

$$(f(x) \cdot g(x))' = f'(x) \cdot g(x) + f(x) \cdot g'(x)$$

**Вывод по определению:**

$$\begin{align}
(f \cdot g)' &= \lim_{h \to 0} \frac{f(x+h) \cdot g(x+h) - f(x) \cdot g(x)}{h} \\
&= \lim_{h \to 0} \frac{f(x+h) \cdot g(x+h) - f(x) \cdot g(x+h) + f(x) \cdot g(x+h) - f(x) \cdot g(x)}{h} \\
&= \lim_{h \to 0} \frac{(f(x+h) - f(x)) \cdot g(x+h) + f(x) \cdot (g(x+h) - g(x))}{h} \\
&= \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} \cdot g(x+h) + f(x) \cdot \lim_{h \to 0} \frac{g(x+h) - g(x)}{h} \\
&= f'(x) \cdot g(x) + f(x) \cdot g'(x)
\end{align}$$

### 2.3. Производная частного

$$\left(\frac{f(x)}{g(x)}\right)' = \frac{f'(x) \cdot g(x) - f(x) \cdot g'(x)}{g^2(x)}$$

**Вывод по определению:**

$$\begin{align}
\left(\frac{f}{g}\right)' &= \lim_{h \to 0} \frac{\frac{f(x+h)}{g(x+h)} - \frac{f(x)}{g(x)}}{h} \\
&= \lim_{h \to 0} \frac{f(x+h) \cdot g(x) - f(x) \cdot g(x+h)}{h \cdot g(x+h) \cdot g(x)} \\
&= \lim_{h \to 0} \frac{f(x+h) \cdot g(x) - f(x) \cdot g(x) + f(x) \cdot g(x) - f(x) \cdot g(x+h)}{h \cdot g(x+h) \cdot g(x)} \\
&= \lim_{h \to 0} \frac{(f(x+h) - f(x)) \cdot g(x) - f(x) \cdot (g(x+h) - g(x))}{h \cdot g(x+h) \cdot g(x)} \\
&= \frac{f'(x) \cdot g(x) - f(x) \cdot g'(x)}{g^2(x)}
\end{align}$$

### 2.4. Производная обратной функции

Если $y = f(x)$ и $x = f^{-1}(y)$, то:

$$(f^{-1})'(y) = \frac{1}{f'(x)}$$

или в другой записи:

$$\frac{dx}{dy} = \frac{1}{\frac{dy}{dx}}$$

**Вывод:**

Из того, что $f(f^{-1}(y)) = y$, дифференцируя обе части по $y$:

$$f'(f^{-1}(y)) \cdot (f^{-1})'(y) = 1$$

откуда:

$$(f^{-1})'(y) = \frac{1}{f'(f^{-1}(y))} = \frac{1}{f'(x)}$$

---

## 3. Таблица производных

### 3.1. Степенная функция (полином)

$$(x^n)' = n \cdot x^{n-1}$$

**Вывод для натурального $n$:**

$$\begin{align}
(x^n)' &= \lim_{h \to 0} \frac{(x+h)^n - x^n}{h} \\
&= \lim_{h \to 0} \frac{x^n + nx^{n-1}h + \frac{n(n-1)}{2}x^{n-2}h^2 + \ldots + h^n - x^n}{h} \\
&= \lim_{h \to 0} \left(nx^{n-1} + \frac{n(n-1)}{2}x^{n-2}h + \ldots + h^{n-1}\right) \\
&= nx^{n-1}
\end{align}$$

**Следствия:**

- $(C)' = 0$ (константа)
- $(x)' = 1$
- $(x^2)' = 2x$
- $(x^3)' = 3x^2$
- $\left(\frac{1}{x}\right)' = (x^{-1})' = -x^{-2} = -\frac{1}{x^2}$
- $(\sqrt{x})' = (x^{1/2})' = \frac{1}{2}x^{-1/2} = \frac{1}{2\sqrt{x}}$

### 3.2. Экспонента

$$(e^x)' = e^x$$

**Вывод:**

$$\begin{align}
(e^x)' &= \lim_{h \to 0} \frac{e^{x+h} - e^x}{h} \\
&= \lim_{h \to 0} \frac{e^x \cdot e^h - e^x}{h} \\
&= e^x \cdot \lim_{h \to 0} \frac{e^h - 1}{h} \\
&= e^x \cdot 1 = e^x
\end{align}$$

где использован замечательный предел: $\lim_{h \to 0} \frac{e^h - 1}{h} = 1$

### 3.3. Логарифм

$$(\ln x)' = \frac{1}{x}$$

**Вывод через обратную функцию:**

Так как $\ln x$ — обратная к $e^x$:

$$(\ln x)' = \frac{1}{(e^y)'} = \frac{1}{e^y} = \frac{1}{e^{\ln x}} = \frac{1}{x}$$

### 3.4. Тангенс

$$(\tan x)' = \frac{1}{\cos^2 x} = \sec^2 x = 1 + \tan^2 x$$

**Вывод через частное:**

$$\begin{align}
(\tan x)' &= \left(\frac{\sin x}{\cos x}\right)' \\
&= \frac{(\sin x)' \cdot \cos x - \sin x \cdot (\cos x)'}{\cos^2 x} \\
&= \frac{\cos x \cdot \cos x - \sin x \cdot (-\sin x)}{\cos^2 x} \\
&= \frac{\cos^2 x + \sin^2 x}{\cos^2 x} \\
&= \frac{1}{\cos^2 x}
\end{align}$$

### 3.5. Арктангенс

$$(\arctan x)' = \frac{1}{1 + x^2}$$

**Вывод через обратную функцию:**

Пусть $y = \arctan x$, тогда $x = \tan y$.

$$(\arctan x)' = \frac{1}{(\tan y)'} = \frac{1}{\frac{1}{\cos^2 y}}= \cos^2 y$$

Из $x = \tan y$ получаем:

$$1 + x^2 = 1 + \tan^2 y = \frac{1}{\cos^2 y}$$

откуда $\cos^2 y = \frac{1}{1 + x^2}$

Следовательно:

$$(\arctan x)' = \frac{1}{1 + x^2}$$
