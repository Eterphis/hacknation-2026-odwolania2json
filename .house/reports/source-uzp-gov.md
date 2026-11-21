# Source: gov.pl/web/uzp - templates and formal rules for our three document classes

Checked 2026-11-21 (coordinator, built-in browser). Pages: `/web/uzp/wzory-dokumentow`, `/web/uzp/podstawowe-informacje3`
(KIO > Postępowanie odwoławcze > Podstawowe informacje). Summary in our words; the page is the source of truth.

## Templates
- KIO "Wzory dokumentów" has **one** template only: "Zamawiający - wzór informacji o postępowaniu" (docx, for the
  contracting authority). **No official template** for the appeal (odwołanie), the power of attorney (pełnomocnictwo)
  or the transfer confirmation. Real documents follow the statutory content below, in free layout: this matches the
  mentors' warning that the test set has changed layouts.

## Appeal (odwołanie): required content (art. 516 ust. 1 Pzp)
Name, seat/address, phone and e-mail of the appellant and the name(s) of its representative(s); name, seat, phone and
e-mail of the contracting authority; PESEL or NIP of an appellant who is a natural person; KRS number (or another
register / NIP) of a non-natural-person appellant; subject of the contract; BZP or OJ EU (TED) notice number; the
contested act or omission; concise charges; the demand; facts, law and evidence; signature; list of attachments.
Since 2026-03 also one e-mail address + one e-Doręczenia address for correspondence (may be the attorney's).
Mandatory attachments: proof of the entry fee (wpis), proof of sending the appeal to the authority, the document
proving authorisation to represent (a complete chain: the power of attorney and the documents showing the grantors'
right to represent, e.g. a KRS extract), proof of the stamp duty on the power of attorney.
-> Implications: Odwołujący/Zamawiający blocks always carry name + seat + contacts; a case can contain extra documents
(KRS extract, proof of sending): they must be rejected as negatives, not misread as one of the three classes.

## Transfer confirmations: two kinds of payment exist
1. **Stamp duty on the power of attorney (opłata skarbowa), 17 zł** - what the UZP training transfers are (judge
   evidence E4). Paper form: to Urząd m.st. Warszawy, Centrum Obsługi Podatnika, account
   `21 1030 1508 0000 0005 5000 0070`; recommended title: "opłata skarbowa za pełnomocnictwo dla: <attorney> do
   reprezentowania: <principal> przed Krajową Izbą Odwoławczą" (+ the proceedings title if the power is for one case).
   Electronic form: to the tax office of the (first Polish) principal's seat - any municipality account.
2. **Entry fee (wpis od odwołania)**: 7 500 / 10 000 / 15 000 / 20 000 zł (supplies/services vs works, below/above EU
   thresholds; 7 500 / 15 000 for social services; 7 500 / 10 000 for omission of a procedure), to UZP's account
   `NBP 60 1010 1010 0081 3622 3100 0000` (IBAN PL60 1010 1010 0081 3622 3100 0000, SWIFT NBPLPLPW); recommended title:
   "Odwołujący: <name> + Zamawiający: <name> + przedmiot: <contract> + Odwołanie z dnia: <date>" (abbreviations such as
   KIO allowed).
-> Implications: (a) the real test set may contain entry-fee transfers, not only 17 zł stamp duty: przelew rules must not
assume 17 zł or one recipient; (b) both recommended titles name the parties (attorney + principal, or Odwołujący +
Zamawiający) and the subject: a strong cross-document signal for T009 and for party roles; (c) the two fixed accounts
and labels ("Urząd Zamówień Publicznych", "Centrum Obsługi Podatnika", "opłata skarbowa", "wpis od odwołania") are good
classification signals and recipient hints.
