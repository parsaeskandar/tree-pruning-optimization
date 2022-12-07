import gzip

# TODO: Find out a way to run bash scripts from python in server. (should change script permissions)
# TODO: There are around 1000 nodes in 6 millions that I prunned but not in the samples list! check them out
# TODO: If There are more header templates like INFO, ... this code wont work (+9 is for that)


if __name__ == '__main__':
    # retained nodes from the backbone script
    with open("retained_nodes_ids.txt", 'r') as f:
        nodes = [node.strip() for node in f]

    print(len(nodes))

    # samples saved from "bcftools query -l public-latest.all.masked.vcf.gz > samples_list.txt" command
    with open("samples_list.txt", 'r') as f:
        samples = [sample.strip() for sample in f]

    sample_dict = {}
    for i, item in enumerate(samples):
        sample_dict[item] = i + 9

    print(len(samples))
    retained_nodes_index_in_samples = list(range(9))
    for node in nodes:
        try:
            retained_nodes_index_in_samples.append(sample_dict[node])
        except KeyError:
            # print(node)
            # print(KeyError)
            # print("There is a retained node that is not in the vcf file!!!")
            continue
    print(len(retained_nodes_index_in_samples))
    with gzip.open('pruned_k10_public-latest.all.masked.vcf.gz', 'wb') as out_file:
        with gzip.open('public-latest.all.masked.vcf.gz', 'rb') as f:
            for line in f:
                if line.startswith(b'##'):
                    out_file.write(line)
                else:
                    a = line.split(b'	')
                    #print(len(list(a[i] for i in retained_nodes_index_in_samples)))
                    #print(len(temp))
                    out_file.write(b'\t'.join(list(a[i].rstrip() for i in retained_nodes_index_in_samples)))
                    out_file.write(b'\n')
                    #exit()
                    #print(len(a))
'''
If want to save nodes index to use with "cut" command know that cut fields lists starts with 1
write this file for using script cut -f `cat nodes_indexes_in_samples.txt` {main tree vcf file} | tee {output vcf file}
cut -f `cat nodes_indexes_in_samples.txt` public-latest.all.masked.vcf.gz | tee pruned_vcf_public-latest.all.masked.vcf
'''
# nodes_index_in_samples = []
# for node in nodes:
#     try:
#         nodes_index_in_samples.append(str(sample_dict[node]))
#     except:
#         continue
# with open("nodes_indexes_in_samples.txt", 'w') as f:
#     f.write(','.join(nodes_index_in_samples))
