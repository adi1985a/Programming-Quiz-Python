import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import matplotlib.pyplot as plt
from datetime import datetime
from database import create_database, insert_question  # Import database functions
from tkinter import ttk
from tkinter import Checkbutton, IntVar

# Global variables
questions = []
current_question = 0
points = 0
current_test_type = None
question_label = None
answer_entry = None
next_button = None
submit_button = None
checkbox_vars = []
checkbox_frame = None

# Establish database connection
conn = create_database()
if conn is None:
    print("Failed to connect to the database.")
    exit()

# Function to generate single-choice test
def generate_single_choice(question, correct, incorrect):
    options = incorrect.split(",") + [correct]
    random.shuffle(options)
    return options

# Function to check the answer
def check_answer(type, user_answer, correct_answer):
    if type == "multiple":
        correct_answers = set(correct_answer.split(","))
        selected_answers = set()
        options = questions[current_question][4].split(",")
        for i, var in enumerate(checkbox_vars):
            if var.get() == 1:
                selected_answers.add(options[i])
        return selected_answers == correct_answers
    elif type == "single":
        # For single choice, exact match is required
        return user_answer.strip().lower() == correct_answer.strip().lower()
    elif type == "open":
        # For open questions, check if key words are present
        user_answer = user_answer.lower()
        correct_answer = correct_answer.lower()
        # Check for at least 3 key words from the correct answer
        key_words = [word for word in correct_answer.split() if len(word) > 3][:5]
        matches = sum(1 for word in key_words if word in user_answer)
        return matches >= 2  # At least 2 key words must match

# Function to start the test
def start_test(type):
    global current_question, questions, points, current_test_type, next_button
    current_question = 0
    points = 0
    current_test_type = type
    
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE type=?", (type,))
    questions = c.fetchall()
    
    if not questions:
        messagebox.showinfo("Error", "No questions available for this test type!")
        return
        
    random.shuffle(questions)
    next_button.config(state=tk.NORMAL)
    show_question()

def show_question():
    global current_question, question_label, answer_entry, questions, next_button, checkbox_frame, checkbox_vars
    if current_question < len(questions):
        question_data = questions[current_question]
        question_label.config(text=f"Question {current_question + 1}/{len(questions)}:\n\n{question_data[1]}")
        
        # Clear previous answer widgets
        if checkbox_frame:
            checkbox_frame.destroy()
        answer_entry.delete(0, tk.END)
        
        if question_data[2] == "multiple":
            # Show checkboxes for multiple choice
            answer_entry.pack_forget()
            answer_label.pack_forget()
            checkbox_frame = tk.Frame(answer_frame)
            checkbox_frame.pack(pady=10)
            checkbox_vars.clear()
            
            options = question_data[4].split(",")
            for option in options:
                var = IntVar()
                checkbox_vars.append(var)
                Checkbutton(checkbox_frame, text=option, variable=var).pack(anchor='w')
        else:
            # Show text entry for other types
            answer_entry.pack(side=tk.LEFT, padx=5)
            answer_label.pack(side=tk.LEFT, padx=5)
            answer_entry.config(state=tk.NORMAL)
        
        next_button.config(state=tk.NORMAL)
    else:
        question_label.config(text=f"Test completed!\nYour score: {points}/{len(questions)}")
        if checkbox_frame:
            checkbox_frame.destroy()
        answer_entry.config(state=tk.DISABLED)
        next_button.config(state=tk.DISABLED)
        save_result(current_test_type, points)

def next_question():
    global current_question, points
    if current_question < len(questions):
        if questions[current_question][2] == "multiple":
            if any(var.get() for var in checkbox_vars):
                correct_answer = questions[current_question][3]
                if check_answer("multiple", None, correct_answer):
                    points += 1
                    messagebox.showinfo("Correct!", "Your answer is correct!")
                else:
                    messagebox.showinfo("Incorrect", f"Correct answers were: {correct_answer}")
                current_question += 1
                show_question()
            else:
                messagebox.showwarning("Warning", "Please select at least one answer.")
        else:
            user_answer = answer_entry.get().strip()
            if user_answer:  # Only check if answer is not empty
                correct_answer = questions[current_question][3]
                if check_answer(current_test_type, user_answer, correct_answer):
                    points += 1
                    messagebox.showinfo("Correct!", "Your answer is correct!")
                else:
                    messagebox.showinfo("Incorrect", f"Correct answer was: {correct_answer}")
                current_question += 1
                show_question()
            else:
                messagebox.showwarning("Warning", "Please enter an answer before continuing.")

# Function to save the result
def save_result(type, points):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = conn.cursor()
    c.execute("INSERT INTO results (type, points, date) VALUES (?, ?, ?)", (type, points, date))
    conn.commit()

# Function to show progress
def show_progress():
    c = conn.cursor()
    c.execute("SELECT date, points FROM results")
    data = c.fetchall()
    dates = [row[0] for row in data]
    points = [row[1] for row in data]
    plt.plot(dates, points, marker='o')
    plt.title("Learning Progress")
    plt.xlabel("Date")
    plt.ylabel("Points")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Before inserting questions, clear existing ones
if conn is not None:
    c = conn.cursor()
    c.execute("DELETE FROM questions")  # Clear existing questions
    
    # Add single choice questions (20+)
    insert_question(conn, "Który protokół routingu używa algorytmu Dijkstry?", "single", "OSPF", 
                   "RIP,BGP,EIGRP")
    
    insert_question(conn, "Jaki typ pamięci jest szybszy?", "single", "SRAM", 
                   "DRAM,ROM,EPROM")
    
    insert_question(conn, "Która warstwa modelu OSI odpowiada za routing?", "single", "Warstwa sieciowa", 
                   "Warstwa transportowa,Warstwa łącza danych,Warstwa fizyczna")
    
    insert_question(conn, "Który model bazy danych używa JSON do przechowywania danych?", "single", "Dokumentowy", 
                   "Relacyjny,Grafowy,Hierarchiczny")
                   
    insert_question(conn, "Który język programowania jest kompilowany?", "single", "C++", 
                   "Python,JavaScript,PHP")
                   
    insert_question(conn, "Który algorytm sortowania ma złożoność O(n log n)?", "single", "QuickSort", 
                   "BubbleSort,SelectionSort,InsertionSort")
                   
    insert_question(conn, "Który typ sieci ma największy zasięg?", "single", "WAN", 
                   "LAN,MAN,PAN")
                   
    insert_question(conn, "Który protokół działa w warstwie aplikacji?", "single", "HTTP", 
                   "TCP,IP,UDP")
                   
    insert_question(conn, "Która metoda szyfrowania jest symetryczna?", "single", "AES", 
                   "RSA,DSA,ECC")
                   
    insert_question(conn, "Który system plików jest natywny dla Linuxa?", "single", "ext4", 
                   "NTFS,FAT32,HFS+")
                   
    insert_question(conn, "Który port jest domyślny dla HTTPS?", "single", "443", 
                   "80,21,22")
                   
    insert_question(conn, "Która technologia wirtualizacji jest typu bare-metal?", "single", "VMware ESXi", 
                   "VirtualBox,QEMU,Wine")
                   
    insert_question(conn, "Który wzorzec projektowy jest kreacyjny?", "single", "Singleton", 
                   "Observer,Iterator,Decorator")
                   
    insert_question(conn, "Która struktura danych działa na zasadzie LIFO?", "single", "Stos", 
                   "Kolejka,Lista,Drzewo")
                   
    insert_question(conn, "Który protokół jest bezstanowy?", "single", "HTTP", 
                   "FTP,SSH,Telnet")
                   
    insert_question(conn, "Która metoda HTTP służy do usuwania zasobów?", "single", "DELETE", 
                   "GET,POST,PUT")
                   
    insert_question(conn, "Który format służy do serializacji danych?", "single", "JSON", 
                   "HTML,CSS,SQL")
                   
    insert_question(conn, "Która technika jest używana do równoważenia obciążenia?", "single", "Round Robin", 
                   "FIFO,LIFO,Priority Queue")
                   
    insert_question(conn, "Który protokół zapewnia poufność danych?", "single", "SSH", 
                   "HTTP,FTP,SMTP")
                   
    insert_question(conn, "Która topologia sieci jest najbardziej niezawodna?", "single", "Mesh", 
                   "Star,Bus,Ring")

    # Add multiple choice questions (20+)
    insert_question(conn, "Które protokoły routingu są protokołami stanu łącza?", 
                   "multiple", "OSPF,IS-IS", 
                   "OSPF,RIP,BGP,IS-IS")
    
    insert_question(conn, "Które z poniższych są typami pamięci RAM?", 
                   "multiple", "DRAM,SRAM", 
                   "DRAM,SRAM,ROM,EPROM")
    
    insert_question(conn, "Które warstwy modelu OSI są związane z końcem komunikacji?", 
                   "multiple", "Warstwa aplikacji,Warstwa prezentacji,Warstwa sesji", 
                   "Warstwa aplikacji,Warstwa prezentacji,Warstwa sesji,Warstwa transportowa")
                   
    insert_question(conn, "Które języki programowania są obiektowe?", 
                   "multiple", "Java,C++,Python", 
                   "Java,C++,Python,Assembly")
                   
    insert_question(conn, "Które systemy operacyjne są oparte na UNIX?", 
                   "multiple", "Linux,macOS,FreeBSD", 
                   "Linux,macOS,FreeBSD,Windows")
                   
    insert_question(conn, "Które protokoły działają w warstwie transportowej?", 
                   "multiple", "TCP,UDP", 
                   "TCP,UDP,IP,HTTP")
                   
    insert_question(conn, "Które metody HTTP są idempotentne?", 
                   "multiple", "GET,PUT,DELETE", 
                   "GET,PUT,DELETE,POST")
                   
    insert_question(conn, "Które algorytmy są używane w kryptografii asymetrycznej?", 
                   "multiple", "RSA,ECC,DSA", 
                   "RSA,ECC,DSA,AES")
                   
    insert_question(conn, "Które wzorce projektowe są strukturalne?", 
                   "multiple", "Adapter,Bridge,Composite", 
                   "Adapter,Bridge,Composite,Singleton")
                   
    insert_question(conn, "Które technologie są związane z konteneryzacją?", 
                   "multiple", "Docker,Kubernetes,Podman", 
                   "Docker,Kubernetes,Podman,VMware")
                   
    insert_question(conn, "Które protokoły są używane w poczcie elektronicznej?", 
                   "multiple", "SMTP,POP3,IMAP", 
                   "SMTP,POP3,IMAP,FTP")
                   
    insert_question(conn, "Które systemy plików obsługują uprawnienia UNIX?", 
                   "multiple", "ext4,XFS,ZFS", 
                   "ext4,XFS,ZFS,FAT32")
                   
    insert_question(conn, "Które języki są używane w uczeniu maszynowym?", 
                   "multiple", "Python,R,Julia", 
                   "Python,R,Julia,HTML")
                   
    insert_question(conn, "Które bazy danych są NoSQL?", 
                   "multiple", "MongoDB,Cassandra,Redis", 
                   "MongoDB,Cassandra,Redis,PostgreSQL")
                   
    insert_question(conn, "Które protokoły są związane z bezpieczeństwem?", 
                   "multiple", "SSL,TLS,IPSec", 
                   "SSL,TLS,IPSec,FTP")
                   
    insert_question(conn, "Które technologie są używane w Big Data?", 
                   "multiple", "Hadoop,Spark,HBase", 
                   "Hadoop,Spark,HBase,MySQL")
                   
    insert_question(conn, "Które elementy są częścią architektury mikrousług?", 
                   "multiple", "API Gateway,Service Registry,Load Balancer", 
                   "API Gateway,Service Registry,Load Balancer,Monolith")
                   
    insert_question(conn, "Które protokoły są używane w IoT?", 
                   "multiple", "MQTT,CoAP,AMQP", 
                   "MQTT,CoAP,AMQP,SQL")
                   
    insert_question(conn, "Które narzędzia służą do CI/CD?", 
                   "multiple", "Jenkins,GitLab CI,Travis CI", 
                   "Jenkins,GitLab CI,Travis CI,Notepad")
                   
    insert_question(conn, "Które języki są kompilowane do kodu natywnego?", 
                   "multiple", "C,C++,Rust", 
                   "C,C++,Rust,Python")

    # Clear and add new multiple choice questions
    if conn is not None:
        c = conn.cursor()
        c.execute("DELETE FROM questions WHERE type='multiple'")  
        
        # Add new multiple choice questions based on the content
        insert_question(conn, "Które z poniższych są cechami programowania obiektowego?", 
                    "multiple", "Hermetyzacja,Dziedziczenie,Polimorfizm", 
                    "Hermetyzacja,Dziedziczenie,Polimorfizm,Sekwencyjność")
        
        insert_question(conn, "Które metody przekazywania parametrów występują w programowaniu?", 
                    "multiple", "Przez wartość,Przez referencję,Przez wskaźnik", 
                    "Przez wartość,Przez referencję,Przez wskaźnik,Przez nazwę")
        
        insert_question(conn, "Które cechy charakteryzują model OSI?", 
                    "multiple", "Fizyczna warstwa,Warstwa łącza danych,Warstwa sieciowa", 
                    "Fizyczna warstwa,Warstwa łącza danych,Warstwa sieciowa,Warstwa abstrakcji")
        
        insert_question(conn, "Które elementy są częścią zasad ACID w bazach danych?", 
                    "multiple", "Atomicity,Consistency,Isolation,Durability", 
                    "Atomicity,Consistency,Isolation,Durability,Flexibility")
        
        insert_question(conn, "Które modele przestrzeni barw są powszechnie używane?", 
                    "multiple", "RGB,CMYK,HSV,LAB", 
                    "RGB,CMYK,HSV,LAB,YUV")
        
        insert_question(conn, "Które cechy charakteryzują systemy wbudowane?", 
                    "multiple", "Niskie zużycie energii,Optymalizacja,Czas rzeczywisty,Miniaturyzacja", 
                    "Niskie zużycie energii,Optymalizacja,Czas rzeczywisty,Miniaturyzacja,Uniwersalność")
        
        insert_question(conn, "Które metody są używane do zapewnienia bezpieczeństwa sieci?", 
                    "multiple", "Firewalle,Szyfrowanie,VPN,IDS/IPS", 
                    "Firewalle,Szyfrowanie,VPN,IDS/IPS,Kompresja")
        
        insert_question(conn, "Jakie są podstawowe pojęcia kryptograficzne?", 
                    "multiple", "Szyfrowanie symetryczne,Szyfrowanie asymetryczne,Funkcje skrótu,Podpis cyfrowy", 
                    "Szyfrowanie symetryczne,Szyfrowanie asymetryczne,Funkcje skrótu,Podpis cyfrowy,Kompresja")
        
        insert_question(conn, "Które czynniki wpływają na wydajność bazy danych?", 
                    "multiple", "Indeksowanie,Optymalizacja zapytań,Szybkie dyski SSD,Buforowanie", 
                    "Indeksowanie,Optymalizacja zapytań,Szybkie dyski SSD,Buforowanie,Fragmentacja")
        
        insert_question(conn, "Jakie są główne cechy komunikacji interpersonalnej?", 
                    "multiple", "Dwustronność,Sygnały werbalne,Sygnały niewerbalne,Kontekst", 
                    "Dwustronność,Sygnały werbalne,Sygnały niewerbalne,Kontekst,Jednokierunkowość")

    # Now add open questions
    # Elektrotechnika i elektronika
    insert_question(conn, "Podaj i omów twierdzenie Thevenina.", "open", "Umożliwia uproszczenie złożonego obwodu elektrycznego do prostego obwodu zastępczego, składającego się ze źródła napięcia i rezystora. Twierdzenie Thevenina mówi, że dowolny liniowy obwód elektryczny, widziany z dwóch zacisków, można zastąpić obwodem równoważnym, składającym się z idealnego źródła napięcia Thevenina (Vth) i rezystora Thevenina (Rth) połączonego szeregowo. Vth - to napięcie otwartego obwodu między zaciskami Rth - to rezystancja widziana między tymi zaciskami, gdy wszystkie niezależne źródła napięcia są zwarte, a niezależne źródła prądu są rozwarte.")
    insert_question(conn, "Scharakteryzuj zasadę prostownika jednopołówkowego.", "open", "Prosty układ prostowniczy, który przewodzi prąd tylko w jednej połowie cyklu napięcia wejściowego. Prostownik jednopołówkowy wykorzystuje diodę, która przewodzi prąd tylko, gdy anoda ma potencjał wyższy niż katoda. W efekcie tylko jedna połowa sinusoidalnego napięcia wejściowego przechodzi przez diodę, tworząc wyprostowane, ale pulsujące napięcie. Jest to najprostszy, ale najmniej efektywny typ prostownika.")
    insert_question(conn, "Wyjaśnij zasady działania pamięci półprzewodnikowych typu RAM", "open", "RAM to ulotna pamięć, w której dane są przechowywane tymczasowo i tracone po wyłączeniu zasilania. RAM (Random Access Memory) działa na zasadzie szybkiego dostępu do danych i wykorzystuje komórki pamięci oparte na tranzystorach i kondensatorach (DRAM) lub na układach flip-flop (SRAM). Jest stosowana do przechowywania aktywnych procesów i danych programów. DRAM wykorzystuje kondensator i wymaga odświeżania, SRAM nie wymaga odświeżania i jest szybsza, ale droższa – ale jak na egzamin ustny, obecna forma jest wystarczająca.")

    # Podstawy programowania
    insert_question(conn, "Scharakteryzuj paradygmaty programowania strukturalnego i obiektowego.", "open", "Programowanie strukturalne opiera się na podziale kodu na funkcje i bloki sterujące, a obiektowe na organizowaniu kodu w klasy i obiekty. Programowanie strukturalne - wykorzystuje konstrukcje takie jak pętle, instrukcje warunkowe i funkcje do organizacji kodu w sposób czytelny i logiczny. Programowanie obiektowe - wprowadza koncepcję obiektów, które łączą dane i metody operujące na tych danych, umożliwiając hermetyzację, dziedziczenie i polimorfizm.")
    insert_question(conn, "Omów metody przekazywania parametrów.", "open", "Parametry można przekazywać przez wartość (kopiowanie danych) lub przez referencję (odwołanie do oryginału). Przez wartość – tworzy kopię wartości parametru, więc zmiany nie wpływają na oryginalne dane. Przez referencję – przekazywana jest referencja do oryginalnej wartości, więc zmiany dokonane wewnątrz funkcji wpływają na zmienną wywołującą. Przez wskaźnik (np. w C++) – przekazywany jest adres pamięci, co daje większą kontrolę nad danymi, ale wymaga ostrożności.")

    # Algorytmy i struktury danych
    insert_question(conn, "Wyjaśnij pojęcia: złożoność czasowa algorytmu (pesymistyczna i średnia).", "open", "Złożoność czasowa określa, ile operacji wykonuje algorytm w zależności od rozmiaru danych. Pesymistyczna ocenia najgorszy możliwy przypadek, a średnia – uśredniony czas działania. Pesymistyczna złożoność (najgorszy przypadek) – określa maksymalną liczbę operacji, jakie algorytm może wykonać. Oznaczana jako O(n) lub inne notacje asymptotyczne. Średnia złożoność – określa oczekiwaną liczbę operacji, bazując na średnich przypadkach wejściowych.")
    insert_question(conn, "Podaj definicję algorytmu oraz metody zapisu.", "open", "Algorytm to skończony zbiór instrukcji prowadzący do rozwiązania określonego problemu. Algorytmy mogą być zapisywane na kilka sposobów: Lista kroków – opis słowny działań. Schemat blokowy – graficzna reprezentacja algorytmu za pomocą bloków i strzałek. Pseudokod – zapis przypominający kod programistyczny, ale niezależny od konkretnego języka. Język programowania – implementacja algorytmu w wybranym języku.")

    # Bazy danych
    insert_question(conn, "Podaj definicję i znaczenie kluczy w relacyjnych bazach danych.", "open", "Klucze w bazach danych służą do jednoznacznej identyfikacji rekordów i zapewnienia integralności danych. Klucz główny (Primary Key) – unikalny identyfikator w tabeli. Klucz obcy (Foreign Key) – odniesienie do klucza głównego w innej tabeli, zapewniające spójność relacji. Klucz kandydujący (Candidate Key) – potencjalny klucz główny, spełniający warunki unikalności. Klucz złożony – składający się z więcej niż jednej kolumny.")
    insert_question(conn, "Podaj charakterystykę języka zapytań SQL.", "open", "SQL to język służący do zarządzania danymi w relacyjnych bazach danych. SQL (Structured Query Language) pozwala na: Pobieranie danych (SELECT) Modyfikację danych (INSERT, UPDATE, DELETE) Definiowanie struktury tabel (CREATE TABLE, ALTER TABLE) Zarządzanie uprawnieniami (GRANT, REVOKE) Obsługę transakcji (COMMIT, ROLLBACK)")
    insert_question(conn, "Wyjaśnij na czym polega proces normalizacji relacyjnej bazy danych.", "open", "Normalizacja to proces organizacji danych w bazie w celu eliminacji redundancji i zapewnienia spójności. Normalizacja składa się z kilku poziomów (normalnych form), np.: 1NF – eliminacja powtarzających się grup danych. 2NF – eliminacja zależności funkcyjnych od części klucza głównego. 3NF – eliminacja zależności pośrednich między kolumnami. BCNF – rozszerzenie 3NF w celu dalszej redukcji zależności.")
    insert_question(conn, "Wyjaśnij pojęcie transakcji.", "open", "Transakcja to zbiór operacji na bazie danych, które muszą być wykonane w całości albo wcale. Transakcja w bazach danych spełnia zasady ACID: Atomicity (Atomowość) – transakcja jest niepodzielna. Consistency (Spójność) – transakcja nie narusza zasad bazy danych. Isolation (Izolacja) – transakcje nie wpływają na siebie nawzajem. Durability (Trwałość) – po zatwierdzeniu transakcji dane są zapisane na stałe.")

    # Programowanie obiektowe
    insert_question(conn, "Wyjaśnij pojęcia obiektu i klasy.", "open", "Klasa to szablon definiujący właściwości i zachowania obiektów, a obiekt to konkretny egzemplarz klasy. Klasa zawiera pola (dane) i metody (funkcje) określające jej zachowanie. Obiekty są instancjami klasy – np. klasa Samochód może mieć obiekty Ford i Toyota, które dziedziczą cechy klasy, ale mogą mieć różne wartości pól (np. kolor).")
    insert_question(conn, "Omów mechanizm metod (funkcji) wirtualnych.", "open", "Metody wirtualne pozwalają na dynamiczne (polimorficzne) wywoływanie metod w klasach dziedziczących. W językach jak C++ i Java metoda oznaczona jako virtual (C++) lub override (C#) może być nadpisywana w klasie pochodnej, a wywołanie metody zależy od typu obiektu w trakcie działania programu, a nie kompilacji.")

    # Sieci komputerowe
    insert_question(conn, "Omów mechanizmy adresacji w sieciach.", "open", "Adresacja w sieciach obejmuje adresy IP, MAC i porty, które umożliwiają identyfikację urządzeń i komunikację. Adres MAC – unikalny identyfikator karty sieciowej na warstwie łącza danych. Adres IP – logiczny adres przypisany urządzeniu w sieci (IPv4, IPv6). Porty – identyfikują konkretne usługi (np. HTTP = port 80).")
    insert_question(conn, "Podaj przykłady protokołów routingu.", "open", "Protokoły routingu określają trasę pakietów w sieci, np. RIP, OSPF, BGP. RIP (Routing Information Protocol) – prosty protokół, bazujący na liczbie przeskoków. OSPF (Open Shortest Path First) – zaawansowany protokół używający algorytmu Dijkstry. BGP (Border Gateway Protocol) – używany do routingu między systemami autonomicznymi w Internecie.")
    insert_question(conn, "Omów model OSI.", "open", "Model OSI to siedmiowarstwowa struktura opisująca komunikację w sieciach. Warstwy modelu OSI: Fizyczna – przesył sygnałów elektrycznych/świetlnych. Łącza danych – adresacja MAC, kontrola dostępu do medium. Sieciowa – adresacja IP, routowanie pakietów. Transportowa – zarządzanie sesjami, protokoły TCP/UDP. Sesji – ustanawianie, utrzymanie i zamykanie sesji. Prezentacji – kodowanie, szyfrowanie danych. Aplikacji – interakcja z użytkownikiem (HTTP, FTP).")

    # Architektura komputerów
    insert_question(conn, "Omów konstrukcję modelu programowego procesora w podejściu CISC i RISC.", "open", "CISC (Complex Instruction Set Computing) ma rozbudowany zestaw instrukcji, a RISC (Reduced Instruction Set Computing) ogranicza liczbę instrukcji dla większej wydajności. CISC – złożone instrukcje, wiele trybów adresowania, np. procesory x86. RISC – proste instrukcje, jednolity czas wykonania, np. ARM, MIPS.")

    # Inżynieria oprogramowania
    insert_question(conn, "Wymień i krótko scharakteryzuj najważniejsze modele cyklu życia oprogramowania.", "open", "Modele cyklu życia oprogramowania określają sposób jego tworzenia i rozwijania, np. model kaskadowy, przyrostowy, spiralny i Agile. Model kaskadowy – liniowy, każda faza kończy się przed rozpoczęciem kolejnej. Model przyrostowy – system rozwijany stopniowo w kolejnych wersjach. Model spiralny – iteracyjne podejście z analizą ryzyka. Agile – elastyczne podejście z iteracjami i częstą interakcją z klientem.")
    insert_question(conn, "Podaj i krótko scharakteryzuj rodzaje testów oprogramowania.", "open", "Testy oprogramowania dzielą się na jednostkowe, integracyjne, systemowe i akceptacyjne. Testy jednostkowe – sprawdzają pojedyncze moduły kodu. Testy integracyjne – testowanie współpracy różnych modułów. Testy systemowe – sprawdzają całość systemu pod kątem funkcjonalności. Testy akceptacyjne – wykonywane przez użytkowników końcowych w celu zatwierdzenia produktu.")

    # Sztuczna inteligencja
    insert_question(conn, "Podaj przykład algorytmu przeszukiwania przestrzeni stanów w systemach sztucznej inteligencji.", "open", "Przeszukiwanie przestrzeni stanów może być realizowane np. przez algorytm A* czy algorytm minimax. Algorytm A* – optymalne przeszukiwanie z heurystyką, używane w wyznaczaniu tras. Minimax – wykorzystywany w grach strategicznych, wybiera najlepszy ruch dla gracza, zakładając, że przeciwnik gra optymalnie.")

    # Grafika komputerowa
    insert_question(conn, "Przedstaw znane modele przestrzeni barw.", "open", "Modele przestrzeni barw to RGB, CMYK, HSV i LAB, stosowane w grafice i druku. RGB (Red, Green, Blue) – model addytywny, stosowany w ekranach. CMYK (Cyan, Magenta, Yellow, Black) – model subtraktywny, używany w druku. HSV (Hue, Saturation, Value) – model oparty na postrzeganiu barw przez człowieka. LAB – model, w którym kolor opisuje jasność oraz dwie osie kolorów, stosowany do precyzyjnej manipulacji barwami")

    # Systemy wbudowane
    insert_question(conn, "Scharakteryzuj systemy wbudowanego.", "open", "Systemy wbudowane to specjalizowane systemy komputerowe przeznaczone do wykonywania określonych zadań. Systemy wbudowane to komputery działające w tle urządzeń, np. w samochodach, sprzęcie AGD, medycznym. Mają zoptymalizowany sprzęt i oprogramowanie, często działają w czasie rzeczywistym.")
    insert_question(conn, "Określ cechy współczesnych systemów wbudowanych", "open", "Nowoczesne systemy wbudowane cechują się energooszczędnością, małymi rozmiarami i wysoką niezawodnością. Najważniejsze cechy to: Niskie zużycie energii – stosowane w urządzeniach przenośnych. Optymalizacja pod kątem konkretnego zadania – brak uniwersalności. Czas rzeczywisty – niektóre systemy muszą reagować natychmiast. Miniaturyzacja – układy SoC (System on Chip) pozwalają zmniejszyć rozmiar i zużycie energii.")

    # Bezpieczeństwo sieci komputerowych
    insert_question(conn, "Przedstaw podstawowe pojęcia kryptograficzne.", "open", "Podstawowe pojęcia to szyfrowanie, klucze, funkcje skrótu i podpis cyfrowy. Szyfrowanie symetryczne – ten sam klucz do szyfrowania i deszyfrowania (AES). Szyfrowanie asymetryczne – para kluczy publiczny-prywatny (RSA). Funkcje skrótu – tworzą unikalny identyfikator danych (SHA-256). Podpis cyfrowy – pozwala na uwierzytelnienie nadawcy i integralność danych.")
    insert_question(conn, "Omów stosowane metody zapewniające bezpieczeństwo sieci komputerowej.", "open", "Do ochrony sieci stosuje się firewalle, szyfrowanie, VPN oraz systemy IDS/IPS. Firewalle – blokują nieautoryzowany ruch. Szyfrowanie – zabezpiecza dane przed przechwyceniem. VPN – tworzy bezpieczne, szyfrowane połączenie. IDS/IPS – systemy wykrywające i zapobiegające atakom.")

    # Systemy baz danych
    insert_question(conn, "Podaj czynniki wpływające na wydajność bazy danych.", "open", "Wydajność zależy od indeksowania, optymalizacji zapytań i sprzętu. Indeksowanie – przyspiesza wyszukiwanie danych. Optymalizacja zapytań – eliminuje zbędne operacje. Zasoby sprzętowe – szybkie dyski SSD poprawiają wydajność. Buforowanie i cache – zmniejsza liczbę operacji na dysku.")
    insert_question(conn, "Omów wybrane modele baz danych.", "open", "Modele baz danych to relacyjne, dokumentowe, grafowe i klucz-wartość. Relacyjne (SQL) – opierają się na tabelach i kluczach (MySQL, PostgreSQL). Dokumentowe (NoSQL) – przechowują dane w formacie JSON/XML (MongoDB). Grafowe – reprezentują dane jako węzły i krawędzie (Neo4j). Klucz-wartość – szybkie mapowanie kluczy na wartości (Redis).")
    insert_question(conn, "Omów metody wykonywania złożonych zapytań SQL pozwalające zwiększyć szybkości ich wykonania.", "open", "Optymalizacja zapytań obejmuje użycie indeksów, partycjonowanie i buforowanie. Indeksowanie – skraca czas wyszukiwania. Partycjonowanie – dzieli duże tabele na mniejsze fragmenty. Materializowane widoki – zapisują wyniki zapytań. EXPLAIN – analiza planu wykonania zapytań pozwala na optymalizację.")

    # Komunikacja interpersonalna
    insert_question(conn, "Scharakteryzuj pojęcie komunikacja interpersonalna i jej cechy.", "open", "Komunikacja interpersonalna to wymiana informacji między ludźmi, obejmująca mowę, gesty i emocje. Główne cechy: Dwustronność – nadawca i odbiorca wymieniają informacje. Sygnały werbalne i niewerbalne – znaczenie ma nie tylko treść, ale i sposób przekazu. Kontekst – kultura, sytuacja, relacje wpływają na interpretację.")

    # Podstawy kreatywności
    insert_question(conn, "Scharakteryzuj pojęcia: inteligencja, rozum, wiedza, mądrość", "open", "Inteligencja – zdolność do rozwiązywania problemów. Rozum – umiejętność logicznego myślenia. Wiedza – zbiór informacji zdobytych przez doświadczenie i naukę. Mądrość – zdolność do wykorzystania wiedzy w praktyce. Inteligencja obejmuje analityczne i społeczne aspekty (IQ, EQ). Rozum pozwala na wyciąganie logicznych wniosków. Wiedza może być deklaratywna (fakty) lub proceduralna (umiejętności). Mądrość to świadome podejmowanie decyzji na podstawie doświadczenia")
    insert_question(conn, "Omów wybrane metody wynalazcze (asymilacja, adaptacja, inwersja)", "open", "Metody wynalazcze to techniki wspomagające kreatywność poprzez wykorzystanie istniejących rozwiązań. Asymilacja – łączenie znanych koncepcji w nowe sposoby. Adaptacja – modyfikowanie istniejących rozwiązań do nowych zastosowań. Inwersja – odwracanie znanych schematów myślowych w celu znalezienia nowego podejścia.")

    conn.commit()

# After inserting questions, verify they are in the database
def check_database():
    c = conn.cursor()
    c.execute("SELECT type, COUNT(*) FROM questions GROUP BY type")
    counts = c.fetchall()
    print("Questions in database:")
    for type, count in counts:
        print(f"{type}: {count} questions")
    return counts

# Call this after inserting questions
check_database()

# GUI
root = tk.Tk()
root.title("Knowledge Tests")
root.geometry("800x600")

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

# Question display
question_label = tk.Label(main_frame, text="Select a test type to begin", 
                         wraplength=700, justify=tk.LEFT, font=('Arial', 12))
question_label.pack(pady=20)

# Answer entry
answer_frame = tk.Frame(main_frame)
answer_frame.pack(pady=20)

answer_label = tk.Label(answer_frame, text="Your answer:", font=('Arial', 10))
answer_label.pack(side=tk.LEFT, padx=5)

answer_entry = tk.Entry(answer_frame, width=50)
answer_entry.pack(side=tk.LEFT, padx=5)

# Buttons frame
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=20)

next_button = tk.Button(button_frame, text="Next Question", command=next_question, state=tk.DISABLED)
next_button.pack(side=tk.LEFT, padx=5)

# Menu
menu = tk.Menu(root)
root.config(menu=menu)

test_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Tests", menu=test_menu)
test_menu.add_command(label="Single Choice", command=lambda: start_test("single"))
test_menu.add_command(label="Open Questions", command=lambda: start_test("open"))
test_menu.add_command(label="Multiple Choice", command=lambda: start_test("multiple"))

# Progress button
tk.Button(main_frame, text="Show Progress", command=show_progress).pack(pady=20)

root.mainloop()

# Close the database connection
conn.close()
