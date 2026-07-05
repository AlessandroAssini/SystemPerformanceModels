import matplotlib.pyplot as plt
import numpy as np

# Data embedded from the assignment
DATA = {
    'RESIDENCE TIME Q-SERVER': {
        'x': [0.01, 1.01, 2.01, 3.01, 4.01, 5.01, 6.01, 7.01, 8.01, 9],
        20: [0.0416, 0.5876, 1.1275, 1.6851, 2.2017, 2.7567, 3.4068, 3.7447, 4.4197, 4.6567],
        50: [0.0427, 0.3730, 0.6960, 1.0686, 1.2968, 1.5417, 1.9677, 2.3214, 2.9241, 3.1075],
        100: [0.0444, 0.2532, 0.4665, 0.6220, 0.9659, 1.0099, 1.3149, 1.6146, 1.8236, 1.6093]
    },
    'RESIDENCE TIME BUFFER': {
        'x': [0.01, 1.01, 2.01, 3.01, 4.01, 5.01, 6.01, 7.01, 8.01, 9],
        20: [13.3266, 9.5783, 8.5386, 7.4321, 6.2337, 5.1624, 4.1855, 3.2161, 2.122, 1.0871],
        50: [10.9783, 5.782, 5.0275, 4.4115, 3.721, 3.1431, 2.5336, 1.8072, 1.2664, 0.657],
        100: [8.5431, 3.4239, 3.0525, 2.6895, 2.3089, 1.9209, 1.5405, 1.1568, 0.7294, 0.3748]
    },
    'SYSTEM RESPONSE TIME': {
        'x': [0.01, 1.01, 2.01, 3.01, 4.01, 5.01, 6.01, 7.01, 8.01, 9],
        20: [41.9723, 6.3914, 6.7423, 6.8649, 7.3723, 8.3322, 8.4369, 9.4966, 10.8624, 11.3080],
        50: [42.5598, 4.1215, 4.0752, 4.5669, 4.5460, 4.3092, 5.0881, 5.1849, 6.4120, 5.9933],
        100: [43.9032, 2.6812, 2.9792, 2.6836, 3.0177, 3.1689, 3.6581, 3.7085, 3.8982, 2.7863]
    },
    'RESPONSE TIME SYSTEM (jobs)': {
        'x': [0.01, 1.01, 2.01, 3.01, 4.01, 5.01, 6.01, 7.01, 8.01, 9],
        20: [13.7051, 11.9511, 13.1196, 14.186, 15.34, 16.246, 16.7277, 18.1177, 19.7557, 19.6414],
        50: [11.208, 7.2662, 7.845, 8.6643, 8.95, 10.4917, 10.6395, 10.0049, 10.7089, 18.9365],
        100: [8.7668, 4.3282, 4.7828, 5.3027, 5.4824, 6.028, 6.3801, 6.8823, 8.9427, 8.3402]
    },
    'NUMERO CUSTOMER P BUFFER': {
        'x': [0.01, 1.01, 2.01, 3.01, 4.01, 5.01, 6.01, 7.01, 8.01, 9],
        20: [0.1347, 9.4767, 16.8835, 22.1279, 25.6342, 26.4430, 25.3551, 22.3309, 17.5383, 9.5384],
        50: [0.1089, 5.7252, 10.1024, 13.2255, 15.0134, 15.7073, 15.2817, 12.1097, 10.154, 6.0254],
        100: [0.0841, 3.4181, 6.0669, 8.1530, 9.2003, 9.5564, 8.8200, 8.0056, 5.9198, 3.2970]
    },
    'FIRING THROUGHPUT TRANSITION BUFFER (transition 9)': {
        'x': [0.01, 1.01, 2.01, 3.01, 4.01, 5.01, 6.01, 7.01, 8.01, 9],
        20: [9.80E-3, 1.0148, 2.0153, 3.0182, 3.9823, 5.0210, 6.0464, 6.9504, 7.9513, 9.2266],
        50: [9.97E-3, 1.0117, 2.0181, 2.9949, 4.0099, 4.9600, 6.0084, 7.0324, 8.0108, 9.0068],
        100: [9.95E-3, 1.0157, 1.9576, 3.0002, 4.0085, 4.9877, 5.9901, 7.0336, 7.9721, 8.9730]
    }
}


def plot_metric(metric_name, filename, ylabel=None, title=None):
    """Plot a single metric with all three timer configurations."""
    data = DATA[metric_name]
    x = data['x']
    
    plt.figure(figsize=(10, 6))
    for timer in [20, 50, 100]:
        plt.plot(x, data[timer], marker='o', label=f'Timer = {timer} sec', linewidth=2, markersize=6)
    
    plt.xlabel('Arrival Rate (jobs/sec)', fontsize=12)
    plt.ylabel(ylabel or metric_name, fontsize=12)
    plt.title(title or metric_name, fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename}")
    plt.close()


def plot_ratio():
    """Plot the ratio NUMERO CUSTOMER P BUFFER / FIRINGH THROUGHPUT TFLUSH."""
    numero = DATA['NUMERO CUSTOMER P BUFFER']
    firingh = DATA['FIRING THROUGHPUT TRANSITION BUFFER (transition 9)']
    x = numero['x']
    
    plt.figure(figsize=(10, 6))
    for timer in [20, 50, 100]:
        ratio = np.array(numero[timer]) / np.array(firingh[timer])
        plt.plot(x, ratio, marker='o', label=f'Timer = {timer} sec', linewidth=2, markersize=6)
    
    plt.xlabel('Arrival Rate (jobs/sec)', fontsize=12)
    plt.ylabel('Numero Customer / Firing Throughput', fontsize=12)
    plt.title('Numero Customer P Buffer / Firing Throughput Transition Buffer', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('numero_over_firingh_ratio.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: numero_over_firingh_ratio.png")
    plt.close()


def main():
    """Generate all requested plots."""
    print("\n" + "="*60)
    print("Generating Performance Evaluation Plots")
    print("="*60 + "\n")
    
    # Plot 1: Response Time System (all classes)
    plot_metric('SYSTEM RESPONSE TIME', 
                'response_time_all_classes.png',
                'Response Time (sec)',
                title='Response Time System (all classes)')
    
    # Plot 2: Response Time System (jobs)
    plot_metric('RESPONSE TIME SYSTEM (jobs)', 
                'response_time_jobs.png',
                'Response Time (sec)',
                title='Response Time System (jobs)')
    
    # Plot 3: Residence QServer
    plot_metric('RESIDENCE TIME Q-SERVER', 
                'residence_qserver.png',
                'Residence Time (sec)',
                title='Residence Time Q-Server')
    
    # Plot 4: Residence Buffer
    plot_metric('RESIDENCE TIME BUFFER', 
                'residence_buffer.png',
                'Residence Time (sec)',
                title='Residence Time Buffer')
    
    # Plot 5: Ratio
    plot_ratio()
    
    print("\n" + "="*60)
    print("All plots generated successfully!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()