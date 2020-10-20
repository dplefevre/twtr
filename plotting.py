from matplotlib import pyplot as plt


def create_plot(sent_list):
    data = [sent_list.count("Positive"), sent_list.count("Negative")]
    indices = ["Positive", "Negative"]
    plt.pie(data, labels=indices)
    plt.show()
