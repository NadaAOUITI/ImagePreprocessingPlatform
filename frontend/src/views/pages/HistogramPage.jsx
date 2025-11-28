// HistogramPage.js
import React from "react";
import { Bar } from "react-chartjs-2";
import { useHistogramStore } from "../../store/useHistogramStore";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function HistogramPage() {
  const { histograms } = useHistogramStore();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-slate-800 mb-8">Analyse d'Histogrammes</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {histograms.map((histo, idx) => {
            const grayData = {
              labels: Array.from({ length: 256 }, (_, i) => i),
              datasets: [
                { 
                  label: "Niveaux de gris", 
                  data: histo.gray, 
                  backgroundColor: "rgba(100, 116, 139, 0.7)",
                  borderColor: "rgba(100, 116, 139, 1)",
                  borderWidth: 1
                }
              ],
            };
            
            const rgbData = {
              labels: Array.from({ length: 256 }, (_, i) => i),
              datasets: [
                { 
                  label: "Rouge", 
                  data: histo.rgb.r, 
                  backgroundColor: "rgba(239, 68, 68, 0.6)",
                  borderColor: "rgba(239, 68, 68, 1)",
                  borderWidth: 1
                },
                { 
                  label: "Vert", 
                  data: histo.rgb.g, 
                  backgroundColor: "rgba(34, 197, 94, 0.6)",
                  borderColor: "rgba(34, 197, 94, 1)",
                  borderWidth: 1
                },
                { 
                  label: "Bleu", 
                  data: histo.rgb.b, 
                  backgroundColor: "rgba(59, 130, 246, 0.6)",
                  borderColor: "rgba(59, 130, 246, 1)",
                  borderWidth: 1
                },
              ],
            };

            const chartOptions = {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'top',
                  labels: {
                    font: {
                      size: 11
                    }
                  }
                }
              },
              scales: {
                x: {
                  display: false
                },
                y: {
                  beginAtZero: true,
                  grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                  }
                }
              }
            };

            return (
              <div key={idx} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                {/* En-tête avec titre */}
                <div className="bg-gradient-to-r from-slate-700 to-slate-600 px-6 py-4">
                  <h3 className="text-xl font-semibold text-white">{histo.title}</h3>
                </div>

                <div className="p-6">
                  {/* Image */}
                  <div className="mb-6 flex justify-center">
                    <img 
                      src={histo.imageSrc} 
                      alt={histo.title} 
                      className="max-w-full h-auto rounded-lg shadow-md border-2 border-slate-200"
                      style={{ maxHeight: '250px' }}
                    />
                  </div>

                  {/* Histogrammes */}
                  <div className="space-y-6">
                    {/* Histogramme en niveaux de gris */}
                    <div className="bg-slate-50 p-4 rounded-lg">
                      <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center">
                        <span className="w-3 h-3 bg-slate-500 rounded-full mr-2"></span>
                        Histogramme en niveaux de gris
                      </h4>
                      <div style={{ height: '180px' }}>
                        <Bar data={grayData} options={chartOptions} />
                      </div>
                    </div>

                    {/* Histogramme RGB */}
                    <div className="bg-slate-50 p-4 rounded-lg">
                      <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center">
                        <span className="w-3 h-3 bg-gradient-to-r from-red-500 via-green-500 to-blue-500 rounded-full mr-2"></span>
                        Histogramme RGB
                      </h4>
                      <div style={{ height: '180px' }}>
                        <Bar data={rgbData} options={chartOptions} />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {histograms.length === 0 && (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">📊</div>
            <p className="text-xl text-slate-600">Aucun histogramme disponible</p>
            <p className="text-sm text-slate-500 mt-2">Veuillez traiter des images pour générer des histogrammes</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default HistogramPage;