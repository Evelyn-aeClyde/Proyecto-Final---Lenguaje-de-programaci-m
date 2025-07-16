% =================================================================
% ==        BASE DE CONOCIMIENTO PARA ANÁLISIS DE ESTUDIANTES      ==
% ==                 VERSIÓN 4.0 (CON ID ÚNICO)                    ==
% =================================================================

:- dynamic estudiante/11.

% --- ESTRUCTURA DEL HECHO ---
% El primer argumento es AHORA el ID único del estudiante (el índice de la fila).
% estudiante(StudentID, College_ID, IQ, Prev_Sem_Result, CGPA, Academic_Performance, Internship_Experience, Extra_Curricular_Score, Communication_Skills, Projects_Completed, Placement).

% =================================================================
% ==                     PERFILES DE ÉXITO                       ==
% =================================================================

candidato_academico_top(StudentID) :-
    estudiante(StudentID, _, _, _, CGPA, _, _, _, _, _, 'yes'),
    CGPA >= 8.5.

candidato_practico(StudentID) :-
    estudiante(StudentID, _, _, _, _, _, 'yes', _, _, Projects, 'yes'),
    Projects >= 4.

lider_comunicador(StudentID) :-
    estudiante(StudentID, _, _, _, _, _, _, ExtraCurr, CommSkills, _, 'yes'),
    CommSkills >= 9,
    ExtraCurr >= 8.

perfil_esforzado(StudentID) :-
    estudiante(StudentID, _, _, PrevSem, CGPA, _, _, _, _, _, 'yes'),
    CGPA > PrevSem + 0.3.

apuesta_segura(StudentID) :-
    estudiante(StudentID, _, _, _, CGPA, _, 'yes', _, CommSkills, Projects, 'yes'),
    CGPA > 7.8,
    CommSkills >= 8,
    Projects >= 2.

tecnico_sin_pasantia(StudentID) :-
    estudiante(StudentID, _, _, _, CGPA, _, 'no', _, _, Projects, 'yes'),
    CGPA > 8.0,
    Projects >= 3.

% =================================================================
% ==                 PERFILES DE ANÁLISIS INTERNO                ==
% =================================================================

estudiante_en_riesgo(StudentID) :-
    estudiante(StudentID, _, _, _, CGPA, AcadPerf, _, _, _, Projects, 'no'),
    CGPA < 6.5,
    AcadPerf < 5,
    Projects < 2.

joya_escondida(StudentID) :-
    estudiante(StudentID, _, IQ, _, CGPA, _, 'no', _, _, _, 'no'),
    IQ >= 125,
    CGPA < 7.0.

riesgo_desmotivacion(StudentID) :-
    estudiante(StudentID, _, _, PrevSem, CGPA, _, _, _, _, _, 'no'),
    PrevSem > 7.0,
    CGPA < PrevSem - 0.5.