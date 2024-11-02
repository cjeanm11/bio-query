from Bio import Entrez, SeqIO

Entrez.email = "jeanmichelcid@gmail.com"
with Entrez.efetch(db="nucleotide", id="NC_000852", rettype="gb", retmode="text") as handle:
    record = SeqIO.read(handle, "genbank")
    
print(f"Sequence ID: {record.id}")
print(f"Description: {record.description}")
print(f"Sequence length: {len(record.seq)}")
print(f"Sequence: {record.seq[:50]}...") 

protein_seq = record.seq.translate()

print(f"Translated protein sequence (first 50 amino acids): {protein_seq[:50]}...")