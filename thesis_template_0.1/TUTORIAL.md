# 📚 Complete Tutorial: IIIT Allahabad Thesis Template on Overleaf

**For B.Tech, M.Tech, and PhD Students**

---

## 📋 TABLE OF CONTENTS

1. [Getting Started on Overleaf](#1-getting-started-on-overleaf)
2. [Filling Your Information](#2-filling-your-information)
3. [Writing Your Abstract & Acknowledgements](#3-writing-your-abstract--acknowledgements)
4. [Working with Chapters](#4-working-with-chapters)
5. [Adding Figures](#5-adding-figures)
6. [Adding Tables](#6-adding-tables)
7. [Adding Equations](#7-adding-equations)
8. [Cross-Referencing](#8-cross-referencing)
9. [Adding References (Bibliography)](#9-adding-references-bibliography)
10. [Lists: Abbreviations, Symbols, Constants](#10-lists-abbreviations-symbols-constants)
11. [Adding Appendices](#11-adding-appendices)
12. [What This Template CANNOT Do](#12-what-this-template-cannot-do)
13. [Common Mistakes to Avoid](#13-common-mistakes-to-avoid)
14. [Best Practices](#14-best-practices)

---

## 1. GETTING STARTED ON OVERLEAF

### Step 1: Upload Template

1. Go to [www.overleaf.com](https://www.overleaf.com)
2. Click **"New Project"** → **"Upload Project"**
3. Select the template ZIP file
4. Wait for files to upload (30 seconds)

### Step 2: First Compilation

1. Click **"Recompile"** button
2. Wait 30-60 seconds
3. PDF should appear on right side
4. If errors appear, check the settings above

---

## 2. FILLING YOUR INFORMATION

### The ONLY Section to Edit for Your Details

Open **`main.tex`** and find lines **88-128**. This is the ONLY place you fill in your information.

```latex
%----------------------------------------------------------------------------------------
%	★★★ FILL IN YOUR INFORMATION HERE ★★★
%----------------------------------------------------------------------------------------

% ============================================================
% THESIS DETAILS
% ============================================================
\thesistitle{Put Your Exact Thesis Title Here}
\degree{Bachelor of Technology}  % Change to: Master of Technology, Doctor of Philosophy

% ============================================================
% SUPERVISOR DETAILS
% ============================================================
\supervisor{Dr. Supervisor Full Name}

% ============================================================
% STUDENT 1 DETAILS (Required)
% ============================================================
\newcommand{\studentonename}{Your Full Name}
\newcommand{\studentoneroll}{IIT2021001}

% ============================================================
% STUDENT 2 DETAILS (Optional - comment out if working alone)
% ============================================================
\newcommand{\studenttwoname}{Second Student Name}
\newcommand{\studenttworoll}{IIT2021002}

% ============================================================
% STUDENT 3 DETAILS (Optional - comment out if only 2 students)
% ============================================================
\newcommand{\studentthreename}{Third Student Name}
\newcommand{\studentthreeroll}{IIT2021003}

% ============================================================
% DEPARTMENT & UNIVERSITY
% ============================================================
\department{Department of Information Technology}
\university{Indian Institute of Information Technology, Allahabad}
```

### Examples by Degree:

#### B.Tech (Single Student):

```latex
\thesistitle{Machine Learning Based Network Intrusion Detection System}
\degree{Bachelor of Technology}
\supervisor{Dr. Rajesh Kumar}

\newcommand{\studentonename}{Amit Sharma}
\newcommand{\studentoneroll}{IIT2021045}

% Comment out student 2 and 3 by adding % at the start
% \newcommand{\studenttwoname}{Second Student Name}
% \newcommand{\studenttworoll}{IIT2021002}
% \newcommand{\studentthreename}{Third Student Name}
% \newcommand{\studentthreeroll}{IIT2021003}
```

#### B.Tech (Group Project - 2 Students):

```latex
\thesistitle{Smart Parking Management System Using IoT}
\degree{Bachelor of Technology}
\supervisor{Dr. Priya Patel}

\newcommand{\studentonename}{Rohan Mehta}
\newcommand{\studentoneroll}{IIT2021101}

\newcommand{\studenttwoname}{Sneha Verma}
\newcommand{\studenttworoll}{IIT2021102}

% Comment out student 3
% \newcommand{\studentthreename}{Third Student Name}
% \newcommand{\studentthreeroll}{IIT2021003}
```

#### M.Tech:

```latex
\thesistitle{Deep Learning Approaches for Medical Image Segmentation}
\degree{Master of Technology}
\supervisor{Dr. Anita Desai}

\newcommand{\studentonename}{Priyanka Joshi}
\newcommand{\studentoneroll}{IMT2020015}

% M.Tech is usually individual work
% \newcommand{\studenttwoname}{Second Student Name}
% \newcommand{\studenttworoll}{IIT2021002}
% \newcommand{\studentthreename}{Third Student Name}
% \newcommand{\studentthreeroll}{IIT2021003}
```

#### PhD:

```latex
\thesistitle{Novel Approaches for Sentiment Analysis in Low-Resource Languages}
\degree{Doctor of Philosophy}
\supervisor{Dr. Vikram Singh}

\newcommand{\studentonename}{Aditya Kumar Gupta}
\newcommand{\studentoneroll}{IRS2018001}

% PhD is individual work
% \newcommand{\studenttwoname}{Second Student Name}
% \newcommand{\studenttworoll}{IIT2021002}
% \newcommand{\studentthreename}{Third Student Name}
% \newcommand{\studentthreeroll}{IIT2021003}

\department{Department of Computer Science and Engineering}
```

### What Updates Automatically:

- ✅ Title page
- ✅ Certificate page
- ✅ Declaration page (uses "I" for 1 student, "We" for multiple)
- ✅ PDF metadata
- ✅ All headers and footers

---

## 3. WRITING YOUR ABSTRACT & ACKNOWLEDGEMENTS

### Abstract

Open **`frontmatter.tex`** and find line **~173**:

```latex
\begin{abstract}
\begin{spacing}{2}

\addchaptertocentry{\abstractname}
A B.Tech thesis should contain an abstract not exceeding 300 words...

\lipsum[1]  ← DELETE THIS LINE

\end{spacing}
\end{abstract}
```

**Replace the placeholder text with your abstract:**

```latex
\begin{abstract}
\begin{spacing}{2}

\addchaptertocentry{\abstractname}

This thesis presents a comprehensive study on machine learning based
network intrusion detection systems. The primary objective is to develop
an efficient and accurate method for detecting network anomalies in
real-time. We propose a novel approach combining deep learning techniques
with traditional signature-based methods...

(Your abstract continues here - max 300 words for B.Tech, 1000 words for PhD)

\end{spacing}
\end{abstract}
```

**Word Limits:**

- B.Tech: 300 words (1 page)
- M.Tech: 500 words (1-2 pages)
- PhD: 1000 words (4 pages)

### Acknowledgements

Find line **~187** in `frontmatter.tex`:

```latex
\begin{acknowledgements}
\begin{spacing}{1.5}
\addchaptertocentry{\acknowledgementname}

The acknowledgments and the people to thank go here...

\lipsum[1]  ← DELETE THIS LINE

\end{spacing}
\end{acknowledgements}
```

**Replace with your acknowledgements:**

```latex
\begin{acknowledgements}
\begin{spacing}{1.5}
\addchaptertocentry{\acknowledgementname}

I would like to express my sincere gratitude to my supervisor,
Dr. Rajesh Kumar, for his continuous support, guidance, and encouragement
throughout this research. His insightful comments and suggestions have been
invaluable in shaping this work.

I am also grateful to the faculty members of the Department of Information
Technology for their support during my studies. Special thanks to my
colleagues and friends who provided a stimulating environment for learning.

Finally, I would like to thank my family for their unconditional love,
support, and patience throughout my academic journey.

\end{spacing}
\end{acknowledgements}
```

---

## 4. WORKING WITH CHAPTERS

### Understanding the Chapter System

Your thesis chapters are in the **`Chapters/`** folder:

- `1_introduction.tex` - Chapter 1
- `2_literature.tex` - Chapter 2
- `3_methods.tex` - Chapter 3

### How to Edit a Chapter

Open any chapter file, for example `Chapters/1_introduction.tex`:

```latex
\chapter{Introduction}  ← This is your chapter title

\label{Chapter1}  ← For cross-referencing (keep this!)

Your content goes here. Start writing your introduction...

\section{Background}  ← Main sections

Your section content...

\subsection{Motivation}  ← Subsections

Your subsection content...
```

### Structure Levels

```latex
\chapter{Chapter Title}           % Level 0 - Main chapter
\section{Section Title}           % Level 1 - Major section
\subsection{Subsection Title}     % Level 2 - Subsection
\subsubsection{Title}             % Level 3 - Minor subsection
```

**Example:**

```latex
\chapter{Methodology}

This chapter describes the methodology used in this research...

\section{Data Collection}

We collected data from three different sources...

\subsection{Dataset 1: Network Traffic Data}

The network traffic data was obtained from...

\subsection{Dataset 2: Malware Samples}

Malware samples were collected from...

\section{Data Preprocessing}

The raw data required several preprocessing steps...
```

### Adding a New Chapter

**Step 1:** Create a new file in the `Chapters/` folder

- Click on **`Chapters/`** folder in Overleaf
- Click **"New File"**
- Name it: `4_results.tex`

**Step 2:** Add this structure to the new file:

```latex
% Chapter 4

\chapter{Results and Discussion}

\label{Chapter4}

This chapter presents the results obtained from our experiments...

\section{Experimental Setup}

The experiments were conducted on...

\section{Results}

The results are presented in the following sections...
```

**Step 3:** Include it in `main.tex`

Find line **~254** in `main.tex` and add:

```latex
\include{Chapters/1_introduction}
\include{Chapters/2_literature}
\include{Chapters/3_methods}
\include{Chapters/4_results}        ← ADD THIS LINE
%\include{Chapters/Chapter5}
```

**Step 4:** Compile (it will now appear in your thesis)

### Typical Chapter Organization

**For B.Tech (6-7 chapters):**

1. Introduction
2. Literature Review
3. System Design / Methodology
4. Implementation
5. Results and Discussion
6. Conclusion and Future Work
7. (Optional) Testing and Validation

**For M.Tech (5-6 chapters):**

1. Introduction
2. Related Work
3. Proposed Methodology
4. Experiments and Results
5. Conclusion and Future Scope

**For PhD (7-10 chapters):**

1. Introduction
2. Background and Related Work
3. Problem Formulation
4. Proposed Approach (can be multiple chapters)
5. Experimental Setup
6. Results and Analysis
7. Discussion
8. Conclusion and Future Directions

---

## 5. ADDING FIGURES

### Basic Figure

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.7\textwidth]{Figures/architecture}
\caption{System Architecture Diagram}
\label{fig:architecture}
\end{figure}
```

### Step-by-Step:

**Step 1:** Upload your image to the `Figures/` folder

- Click **`Figures/`** folder in Overleaf
- Click **"Upload"** button
- Select your image file (PNG, JPG, or PDF)
- Supported formats: `.png`, `.jpg`, `.pdf`

**Step 2:** Insert figure in your chapter:

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{Figures/network_diagram}
\caption{Network Architecture showing different components}
\label{fig:network}
\end{figure}
```

### Figure Placement Options

```latex
[h]   % Here - try to place it here
[t]   % Top - place at top of page
[b]   % Bottom - place at bottom of page
[p]   % Page - place on a separate page
[H]   % HERE - force it exactly here (requires \usepackage{float})
```

**Recommended:** Use `[h]` for most cases, `[H]` if position is critical

### Controlling Figure Size

```latex
% By width (recommended)
\includegraphics[width=0.5\textwidth]{Figures/image}   % Half page width
\includegraphics[width=0.8\textwidth]{Figures/image}   % 80% of page width
\includegraphics[width=12cm]{Figures/image}            % Fixed 12cm width

% By height
\includegraphics[height=6cm]{Figures/image}

% By scale
\includegraphics[scale=0.5]{Figures/image}             % 50% of original size
```

### Side-by-Side Figures

```latex
\begin{figure}[h]
\centering
\begin{minipage}{0.45\textwidth}
    \centering
    \includegraphics[width=\textwidth]{Figures/before}
    \caption{Before optimization}
    \label{fig:before}
\end{minipage}
\hfill
\begin{minipage}{0.45\textwidth}
    \centering
    \includegraphics[width=\textwidth]{Figures/after}
    \caption{After optimization}
    \label{fig:after}
\end{minipage}
\end{figure}
```

### Subfigures (Multiple images, one caption)

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.4\textwidth]{Figures/result1}
\hspace{1cm}
\includegraphics[width=0.4\textwidth]{Figures/result2}
\caption{Results comparison: (left) Method A, (right) Method B}
\label{fig:comparison}
\end{figure}
```

### Caption Guidelines

**Good captions:**

- Be descriptive
- Explain what the reader should see
- Use proper grammar

```latex
% Good
\caption{Accuracy vs Training Epochs for different learning rates}

% Good
\caption{System architecture showing data flow between components}

% Bad (too short)
\caption{Results}

% Bad (too vague)
\caption{Graph}
```

### Referencing Figures in Text

```latex
The system architecture is shown in Figure~\ref{fig:architecture}.

As can be seen in Figure~\ref{fig:results}, the accuracy improves with training.

Figure~\ref{fig:network} illustrates the network topology used in our experiments.
```

**Note:** Always use `Figure~\ref{...}` (with `~` for non-breaking space)

---

## 6. ADDING TABLES

### Basic Table

```latex
\begin{table}[h]
\centering
\caption{Comparison of different algorithms}
\label{tab:comparison}
\begin{tabular}{l c c c}
\toprule
\textbf{Algorithm} & \textbf{Accuracy} & \textbf{Time (s)} & \textbf{Memory (MB)} \\
\midrule
Method A & 92.5\% & 12.3 & 256 \\
Method B & 94.2\% & 15.7 & 312 \\
Method C & 91.8\% & 10.1 & 198 \\
\bottomrule
\end{tabular}
\end{table}
```

### Table Structure Explained

```latex
\begin{tabular}{l c c c}
                  ↑ ↑ ↑ ↑
                  └─ Column alignments
                     l = left
                     c = center
                     r = right

Content & Content & Content & Content \\  % Columns separated by &, rows end with \\
\hline                                    % Horizontal line
```

### Table Examples

#### Performance Comparison Table

```latex
\begin{table}[h]
\centering
\caption{Performance metrics of proposed system}
\label{tab:performance}
\begin{tabular}{l c c c}
\toprule
\textbf{Metric} & \textbf{Training} & \textbf{Validation} & \textbf{Testing} \\
\midrule
Accuracy       & 95.2\%  & 93.8\%  & 94.1\% \\
Precision      & 94.5\%  & 92.9\%  & 93.2\% \\
Recall         & 96.1\%  & 94.2\%  & 94.8\% \\
F1-Score       & 95.3\%  & 93.5\%  & 94.0\% \\
\bottomrule
\end{tabular}
\end{table}
```

#### Dataset Description Table

```latex
\begin{table}[h]
\centering
\caption{Description of datasets used in experiments}
\label{tab:datasets}
\begin{tabular}{l r r r}
\toprule
\textbf{Dataset} & \textbf{Samples} & \textbf{Features} & \textbf{Classes} \\
\midrule
Dataset 1 & 10,000 & 128 & 5 \\
Dataset 2 & 25,000 & 256 & 10 \\
Dataset 3 & 15,000 & 64  & 3 \\
\bottomrule
\end{tabular}
\end{table}
```

#### Multi-row Table

```latex
\begin{table}[h]
\centering
\caption{Hardware and software specifications}
\label{tab:specs}
\begin{tabular}{l p{8cm}}
\toprule
\textbf{Component} & \textbf{Specification} \\
\midrule
Processor   & Intel Core i7-9700K @ 3.60GHz \\
RAM         & 32 GB DDR4 \\
GPU         & NVIDIA GeForce RTX 2080 Ti (11GB) \\
Operating System & Ubuntu 20.04 LTS \\
Deep Learning Framework & TensorFlow 2.8, PyTorch 1.10 \\
Programming Language & Python 3.9 \\
\bottomrule
\end{tabular}
\end{table}
```

### Long Tables (Spanning Multiple Pages)

For tables that don't fit on one page, use `longtable`:

```latex
\begin{longtable}{l c c}
\caption{List of all experiments and their results} \\
\toprule
\textbf{Experiment} & \textbf{Accuracy} & \textbf{Time (s)} \\
\midrule
\endfirsthead

\multicolumn{3}{c}{{\tablename\ \thetable{} -- continued from previous page}} \\
\toprule
\textbf{Experiment} & \textbf{Accuracy} & \textbf{Time (s)} \\
\midrule
\endhead

\bottomrule
\endfoot

Exp 1 & 92.5\% & 12.3 \\
Exp 2 & 93.1\% & 14.2 \\
... (many more rows)
\end{longtable}
```

### Referencing Tables in Text

```latex
The results are summarized in Table~\ref{tab:results}.

As shown in Table~\ref{tab:comparison}, our method outperforms existing approaches.

Table~\ref{tab:datasets} provides details about the datasets used.
```

---

## 7. ADDING EQUATIONS

### Inline Equations

```latex
The equation $E = mc^2$ is Einstein's famous formula.

We calculate the mean using $\mu = \frac{1}{n}\sum_{i=1}^{n} x_i$.
```

### Display Equations (Numbered)

```latex
\begin{equation}
E = mc^2
\label{eq:einstein}
\end{equation}

\begin{equation}
\mu = \frac{1}{n}\sum_{i=1}^{n} x_i
\label{eq:mean}
\end{equation}
```

### Display Equations (Unnumbered)

```latex
\[ E = mc^2 \]

\[ \mu = \frac{1}{n}\sum_{i=1}^{n} x_i \]
```

### Common Mathematical Symbols

```latex
% Greek letters
\alpha, \beta, \gamma, \delta, \epsilon, \theta, \lambda, \mu, \sigma, \omega

% Superscripts and subscripts
x^2, x_i, x^{2n}, x_{i,j}

% Fractions
\frac{numerator}{denominator}

% Square root
\sqrt{x}, \sqrt[3]{x}

% Summation and integration
\sum_{i=1}^{n} x_i
\int_{a}^{b} f(x) dx

% Limits
\lim_{x \to \infty} f(x)

% Matrices
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
```

### Complex Equation Example

```latex
\begin{equation}
f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
\label{eq:gaussian}
\end{equation}
```

### Referencing Equations

```latex
As shown in Equation~\ref{eq:gaussian}, the Gaussian distribution...

Using Equation~\ref{eq:mean}, we calculate the mean value.
```

---

## 8. CROSS-REFERENCING

### The Label-Reference System

**Step 1:** Add a label to what you want to reference

```latex
\chapter{Introduction}
\label{chap:intro}  ← Label for this chapter

\section{Background}
\label{sec:background}  ← Label for this section

\begin{figure}[h]
...
\label{fig:architecture}  ← Label for this figure
\end{figure}

\begin{table}[h]
...
\label{tab:results}  ← Label for this table
\end{table}

\begin{equation}
...
\label{eq:formula}  ← Label for this equation
\end{equation}
```

**Step 2:** Reference it anywhere in your thesis

```latex
As discussed in Chapter~\ref{chap:intro}...

See Section~\ref{sec:background} for more details...

Figure~\ref{fig:architecture} shows the system design...

The results in Table~\ref{tab:results} indicate...

Using Equation~\ref{eq:formula}, we can calculate...
```

### Label Naming Conventions

Use prefixes to identify what you're referencing:

```latex
\label{chap:introduction}      % For chapters
\label{sec:methodology}         % For sections
\label{subsec:algorithm}        % For subsections
\label{fig:diagram}             % For figures
\label{tab:results}             % For tables
\label{eq:equation}             % For equations
\label{alg:algorithm}           % For algorithms
\label{app:appendix}            % For appendices
```

### Page References

```latex
See page~\pageref{fig:architecture} for the diagram.

The methodology is discussed on page~\pageref{sec:methodology}.
```

### Multiple References

```latex
As shown in Figures~\ref{fig:before} and~\ref{fig:after}...

See Tables~\ref{tab:dataset1},~\ref{tab:dataset2}, and~\ref{tab:dataset3}...
```

---

## 9. ADDING REFERENCES (BIBLIOGRAPHY)

### Understanding BibTeX

Your references are stored in **`example.bib`** file. Each reference has:

- **Type** (article, book, inproceedings, etc.)
- **Key** (unique identifier you use to cite it)
- **Fields** (author, title, year, etc.)

### Adding References to example.bib

Open **`example.bib`** and add your references:

#### Journal Article

```bibtex
@article{smith2020deep,
  author  = {Smith, John and Doe, Jane},
  title   = {Deep Learning for Network Security},
  journal = {IEEE Transactions on Network Security},
  year    = {2020},
  volume  = {15},
  number  = {3},
  pages   = {234--251},
  doi     = {10.1109/TNS.2020.12345}
}
```

#### Conference Paper

```bibtex
@inproceedings{kumar2019machine,
  author    = {Kumar, Raj and Patel, Priya},
  title     = {Machine Learning Approaches for Intrusion Detection},
  booktitle = {Proceedings of the International Conference on Network Security},
  year      = {2019},
  pages     = {45--52},
  publisher = {ACM},
  address   = {New York, NY, USA}
}
```

#### Book

```bibtex
@book{goodfellow2016deep,
  author    = {Goodfellow, Ian and Bengio, Yoshua and Courville, Aaron},
  title     = {Deep Learning},
  year      = {2016},
  publisher = {MIT Press},
  address   = {Cambridge, MA, USA}
}
```

#### Book Chapter

```bibtex
@incollection{lecun2015deep,
  author    = {LeCun, Yann and Bengio, Yoshua and Hinton, Geoffrey},
  title     = {Deep Learning},
  booktitle = {Nature},
  year      = {2015},
  volume    = {521},
  pages     = {436--444}
}
```

#### Website/Online Resource

```bibtex
@misc{tensorflow2021,
  author       = {{TensorFlow}},
  title        = {TensorFlow: An Open Source Machine Learning Framework},
  year         = {2021},
  howpublished = {\url{https://www.tensorflow.org}},
  note         = {Accessed: 2021-09-15}
}
```

#### Thesis/Dissertation

```bibtex
@phdthesis{sharma2018thesis,
  author  = {Sharma, Amit},
  title   = {Novel Approaches in Network Security},
  school  = {Indian Institute of Technology},
  year    = {2018},
  address = {Delhi, India}
}
```

### Citing References in Your Thesis

```latex
Deep learning has revolutionized many fields~\cite{goodfellow2016deep}.

Several researchers have proposed methods~\cite{smith2020deep,kumar2019machine}.

According to LeCun et al.~\cite{lecun2015deep}, deep learning has...

The TensorFlow framework~\cite{tensorflow2021} was used for implementation.
```

### Citation Styles

```latex
\cite{key}                    % [1]
\cite{key1,key2,key3}         % [1, 2, 3]
Author~\cite{key}             % Author [1]
```

### Getting BibTeX from Sources

**Google Scholar:**

1. Search for your paper
2. Click "Cite" (quotation mark icon)
3. Click "BibTeX" at bottom
4. Copy and paste into `example.bib`

**IEEE Xplore / ACM Digital Library:**

1. Find your paper
2. Look for "Export Citation" or "Download Citation"
3. Select "BibTeX" format
4. Copy and paste

---

## 10. LISTS: ABBREVIATIONS, SYMBOLS, CONSTANTS

### List of Abbreviations

Open **`frontmatter.tex`** and find line **~212**:

```latex
\begin{abbreviations}{ll}

\textbf{LAH} & \textbf{L}ist \textbf{A}bbreviations \textbf{H}ere\\
\textbf{WSF} & \textbf{W}hat (it) \textbf{S}tands \textbf{F}or\\

\end{abbreviations}
```

**Replace with your abbreviations:**

```latex
\begin{abbreviations}{ll}

\textbf{AI} & \textbf{A}rtificial \textbf{I}ntelligence\\
\textbf{ML} & \textbf{M}achine \textbf{L}earning\\
\textbf{DL} & \textbf{D}eep \textbf{L}earning\\
\textbf{CNN} & \textbf{C}onvolutional \textbf{N}eural \textbf{N}etwork\\
\textbf{RNN} & \textbf{R}ecurrent \textbf{N}eural \textbf{N}etwork\\
\textbf{LSTM} & \textbf{L}ong \textbf{S}hort-\textbf{T}erm \textbf{M}emory\\
\textbf{IDS} & \textbf{I}ntrusion \textbf{D}etection \textbf{S}ystem\\
\textbf{IoT} & \textbf{I}nternet \textbf{o}f \textbf{T}hings\\

\end{abbreviations}
```

### List of Symbols

Find line **~236** in `frontmatter.tex`:

```latex
\begin{symbols}{lll}

$a$ & distance & \si{\meter} \\
$P$ & power & \si{\watt} (\si{\joule\per\second}) \\

\addlinespace

$\omega$ & angular frequency & \si{\radian} \\

\end{symbols}
```

**Replace with your symbols:**

```latex
\begin{symbols}{lll}

$x$ & input vector & dimensionless \\
$y$ & output/target & dimensionless \\
$w$ & weight vector & dimensionless \\
$b$ & bias term & dimensionless \\
$\alpha$ & learning rate & dimensionless \\
$\lambda$ & regularization parameter & dimensionless \\
$\sigma$ & sigmoid function & dimensionless \\

\addlinespace  % Separate Roman and Greek symbols

$\theta$ & model parameters & dimensionless \\
$\epsilon$ & error term & dimensionless \\
$\mu$ & mean & dimensionless \\
$\sigma^2$ & variance & dimensionless \\

\end{symbols}
```

### Physical Constants (If applicable)

Find line **~223** in `frontmatter.tex`:

```latex
\begin{constants}{lr@{${}={}$}l}

Speed of Light & $c_{0}$ & \SI{2.99792458e8}{\meter\per\second} (exact)\\
Constant Name & $Symbol$ & $Constant Value$ with units\\

\end{constants}
```

**For most CS/IT theses, you can delete this section or leave it empty.**

For Physics/Engineering theses:

```latex
\begin{constants}{lr@{${}={}$}l}

Speed of Light & $c$ & \SI{2.99792458e8}{\meter\per\second}\\
Planck's Constant & $h$ & \SI{6.62607015e-34}{\joule\second}\\
Boltzmann Constant & $k_B$ & \SI{1.380649e-23}{\joule\per\kelvin}\\

\end{constants}
```

---

## 11. ADDING APPENDICES

### What Goes in Appendices?

- Supplementary material that's too detailed for main chapters
- Code listings
- Additional mathematical derivations
- Extra experimental results
- Questionnaires or survey forms
- Detailed algorithms

### Editing Existing Appendix

Open **`Appendices/AppendixA.tex`**:

```latex
% Appendix A

\chapter{Frequently Asked Questions}

\label{AppendixA}

\section{How do I change the colors of links?}
...
```

**Replace with your content:**

```latex
% Appendix A

\chapter{Implementation Details}

\label{AppendixA}

\section{Complete Algorithm Pseudocode}

The complete pseudocode for the proposed algorithm is as follows:

...your content...

\section{Additional Experimental Results}

This section presents additional results that complement the main findings...
```

### Adding a New Appendix

**Step 1:** Create `Appendices/AppendixB.tex`:

```latex
% Appendix B

\chapter{Source Code Listings}

\label{AppendixB}

\section{Data Preprocessing Module}

The following code shows the implementation of the data preprocessing module:

\begin{verbatim}
import pandas as pd
import numpy as np

def preprocess_data(data):
    # Remove missing values
    data = data.dropna()
    # Normalize features
    data = (data - data.mean()) / data.std()
    return data
\end{verbatim}

\section{Model Training Module}

The model training code is implemented as follows:

...
```

**Step 2:** Include it in `main.tex` (line ~269):

```latex
\include{Appendices/AppendixA}
\include{Appendices/AppendixB}  ← ADD THIS LINE
%\include{Appendices/AppendixC}
```

### Referencing Appendices

```latex
See Appendix~\ref{AppendixA} for detailed implementation.

The complete code is provided in Appendix~\ref{AppendixB}.
```

---

## 12. WHAT THIS TEMPLATE CANNOT DO

### ❌ Limitations

#### 1. **Hindi Text** (This pdfLaTeX version)

```latex
% This will NOT work:
\begin{hindi}
भारतीय सूचना प्रौद्योगिकी संस्थान
\end{hindi}
```

**Reason:** This version uses pdfLaTeX, not XeLaTeX. Hindi fonts require XeLaTeX.

#### 2. **Complex TikZ Diagrams** (Limited)

While basic TikZ works, very complex diagrams may cause compilation issues.
**Solution:** Create diagrams in external tools (draw.io, PowerPoint) and insert as images.

#### 3. **Automatic Glossary Generation**

The template doesn't have an automated glossary system.
**Solution:** Use the abbreviations list manually.

#### 4. **Automatic Index Generation**

No automatic index creation for keywords.
**Solution:** Use the table of contents for navigation.

#### 5. **Videos or Interactive Content**

PDFs cannot embed videos or interactive elements.
**Solution:** Include screenshots and QR codes linking to online content.

#### 6. **Custom Fonts**

Limited font options in pdfLaTeX.
**Solution:** Use standard LaTeX fonts (default Palatino is elegant).

#### 7. **More Than 3 Students**

The template supports up to 3 students only.
**Solution:** For more students, you'll need to edit `main.tex` to add more student commands.

---

## 13. COMMON MISTAKES TO AVOID

### ❌ Mistake 1: Forgetting to Change Bibliography to Biber

**Symptom:** References don't appear in bibliography
**Fix:** Menu → Settings → Bibliography → Change to "Biber"

### ❌ Mistake 2: Not Compiling Twice

**Symptom:** "??" appears instead of figure/table numbers
**Fix:** Click "Recompile" at least twice

### ❌ Mistake 3: Wrong File Extensions

```latex
% Wrong
\includegraphics{Figures/image.png}

% Correct
\includegraphics{Figures/image}  % Don't include extension
```

### ❌ Mistake 4: Spaces in Filenames

```latex
% Bad
\includegraphics{Figures/my image.png}

% Good
\includegraphics{Figures/my_image}
```

### ❌ Mistake 5: Forgetting Labels

```latex
% Wrong - can't reference it later
\begin{figure}[h]
\includegraphics{...}
\caption{My figure}
\end{figure}

% Correct
\begin{figure}[h]
\includegraphics{...}
\caption{My figure}
\label{fig:myfigure}  ← ADD THIS
\end{figure}
```

### ❌ Mistake 6: Using Absolute Paths

```latex
% Wrong
\includegraphics{C:/Users/Student/Desktop/image.png}

% Correct
\includegraphics{Figures/image}
```

### ❌ Mistake 7: Not Using Non-Breaking Space (~)

```latex
% Wrong
Figure \ref{fig:test} shows...    % Might break across lines

% Correct
Figure~\ref{fig:test} shows...    % Keeps "Figure" and number together
```

### ❌ Mistake 8: Editing frontmatter.tex for Names

**Wrong approach:** Editing placeholders in `frontmatter.tex`
**Correct approach:** Fill ONE section in `main.tex` (lines 88-128)

### ❌ Mistake 9: Special Characters Without Escape

```latex
% These need backslash:
% & $ # _ { } ~ ^ \

% Wrong
The cost is $100 & the time is 5 minutes.

% Correct
The cost is \$100 \& the time is 5 minutes.
```

### ❌ Mistake 10: Forgetting to Add New Chapters to main.tex

Creating a new chapter file isn't enough - you must also add `\include{Chapters/newchapter}` in `main.tex`.

---

## 14. BEST PRACTICES

### ✅ Writing

1. **Write in Present Tense for Methods**

   ```
   Good: "We use deep learning..."
   Bad: "We used deep learning..."
   ```

2. **Use Past Tense for Results**

   ```
   Good: "The experiments showed that..."
   Bad: "The experiments show that..."
   ```

3. **Be Consistent with Terminology**
   - Pick one term and stick with it
   - "Machine Learning" (not switching to "ML" randomly)
   - Define abbreviations on first use

4. **Write Descriptive Captions**
   ```
   Good: "Training accuracy vs epochs for different learning rates (0.001, 0.01, 0.1)"
   Bad: "Results"
   ```

### ✅ Organization

1. **One Chapter = One Main File**
   Don't split chapters across multiple files

2. **Logical Figure Naming**

   ```
   Figures/ch1_architecture.png
   Figures/ch2_algorithm_flowchart.png
   Figures/ch4_result_accuracy.png
   ```

3. **Keep Related Content Together**
   - Put related figures near the text that discusses them
   - Don't scatter related content across chapters

### ✅ Compilation

1. **Compile Regularly**
   - Compile every time you add a figure, table, or reference
   - Catch errors early!

2. **Check PDF After Each Major Change**
   - Verify figures appear correctly
   - Check that references are resolved
   - Look for overfull/underfull boxes

3. **Compile Twice for Cross-References**
   - First compile: LaTeX creates .aux files
   - Second compile: Resolves references

### ✅ Version Control

1. **Use Overleaf's History Feature**
   - Overleaf saves every version
   - History → Version History → Browse previous versions

2. **Name Versions Meaningfully**
   - Add labels to versions: "Chapter 3 complete", "After review", etc.

3. **Backup Regularly**
   - Download PDF and source weekly
   - Keep backups on your computer

### ✅ Collaboration (For Group Projects)

1. **Divide Chapters Clearly**
   - Each student writes specific chapters
   - One person manages main.tex and frontmatter.tex

2. **Communicate Changes**
   - Use Overleaf's chat feature
   - Discuss before making major structural changes

3. **Review Together**
   - Check consistency of writing style
   - Ensure references are formatted consistently

### ✅ Before Final Submission

- [ ] All student names and roll numbers correct
- [ ] Supervisor name correct
- [ ] Thesis title exact (check official records)
- [ ] All figures have captions and labels
- [ ] All tables have captions and labels
- [ ] All references cited appear in bibliography
- [ ] No "??" in the document (unresolved references)
- [ ] Table of contents is up-to-date
- [ ] List of figures is complete
- [ ] List of tables is complete
- [ ] Abstract within word limit
- [ ] Acknowledgements written
- [ ] Compiled at least twice
- [ ] Downloaded final PDF
- [ ] Spell-check completed

---

## 🎓 FINAL TIPS

### For B.Tech Students:

- Keep it concise (60-80 pages typical)
- Focus on implementation details
- Include plenty of screenshots and diagrams
- Show your code in appendices

### For M.Tech Students:

- More depth than B.Tech (80-120 pages typical)
- Emphasize research contribution
- Include thorough literature review
- Present comprehensive experimental results

### For PhD Students:

- Substantial contribution required (150-250+ pages typical)
- Multiple research chapters
- Extensive literature review
- Detailed mathematical proofs (if applicable)
- Comprehensive experiments and analysis

---

## 🆘 GETTING HELP

### Overleaf Documentation:

- [https://www.overleaf.com/learn](https://www.overleaf.com/learn)

### LaTeX Resources:

- **Overleaf Tutorial:** [https://www.overleaf.com/learn/latex/Tutorials](https://www.overleaf.com/learn/latex/Tutorials)
- **LaTeX Wikibook:** [https://en.wikibooks.org/wiki/LaTeX](https://en.wikibooks.org/wiki/LaTeX)
- **Detexify** (find symbols): [http://detexify.kirelabs.org/classify.html](http://detexify.kirelabs.org/classify.html)

### Common LaTeX Errors and Solutions:

1. **"File not found"** → Check file path and spelling
2. **"Undefined control sequence"** → Typo in command name
3. **"Missing $ inserted"** → Forgot to close math mode
4. **"Bibliography not found"** → Changed to Biber in settings?

---

## 🎉 YOU'RE READY!

You now know everything needed to create your thesis using this template.

**Remember:**

- Fill in ONE section (main.tex lines 88-128)
- Everything else updates automatically
- Compile often
- Ask for help when stuck

**Good luck with your thesis! 🎓**

---

_This tutorial covers all essential features of the IIIT Allahabad thesis template. For advanced LaTeX features, consult the Overleaf documentation._
