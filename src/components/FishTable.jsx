import React, { useState, useMemo } from 'react';
import { ArrowUpDown, Search, AlertTriangle, ShieldCheck, Info } from 'lucide-react';

const FishTable = ({ data }) => {
    const [sortConfig, setSortConfig] = useState({ key: 'mean_ppm', direction: 'ascending' });
    const [searchTerm, setSearchTerm] = useState('');

    const sortedData = useMemo(() => {
        let sortableItems = [...data];

        // Parse numeric values for sorting
        sortableItems = sortableItems.map(item => ({
            ...item,
            mean_val: parseFloat(item.mean_ppm) || 0
        }));

        if (sortConfig.key) {
            sortableItems.sort((a, b) => {
                let aValue = a[sortConfig.key];
                let bValue = b[sortConfig.key];

                // Use parsed value if sorting by mean
                if (sortConfig.key === 'mean_ppm') {
                    aValue = a.mean_val;
                    bValue = b.mean_val;
                }

                if (aValue < bValue) {
                    return sortConfig.direction === 'ascending' ? -1 : 1;
                }
                if (aValue > bValue) {
                    return sortConfig.direction === 'ascending' ? 1 : -1;
                }
                return 0;
            });
        }

        // Filter
        if (searchTerm) {
            sortableItems = sortableItems.filter(item =>
                item.species.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        return sortableItems;
    }, [data, sortConfig, searchTerm]);

    const requestSort = (key) => {
        let direction = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    const getMercuryLevel = (val) => {
        // FDA Guidance roughly:
        // < 0.15 : Best choices
        // 0.15 - 0.46 : Good choices
        // > 0.46 : Avoid
        if (val < 0.15) return { color: 'text-safe-green', bg: 'bg-safe-green/10', label: 'Low' };
        if (val < 0.46) return { color: 'text-warning-yellow', bg: 'bg-warning-yellow/10', label: 'Medium' };
        return { color: 'text-alert-red', bg: 'bg-alert-red/10', label: 'High' };
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-6 bg-ocean-blue rounded-xl shadow-2xl border border-white/5">
            <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    Fish Rankings
                </h2>
                <div className="relative w-full md:w-64">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
                    <input
                        type="text"
                        placeholder="Search species..."
                        className="w-full pl-10 pr-4 py-2 bg-ocean-dark border border-white/10 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-accent-teal transition-all placeholder:text-slate-500"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b border-white/10 text-slate-400 text-sm uppercase tracking-wider">
                            <th
                                className="p-4 cursor-pointer hover:text-white transition-colors"
                                onClick={() => requestSort('species')}
                            >
                                <div className="flex items-center gap-2">
                                    Species
                                    <ArrowUpDown className="w-4 h-4" />
                                </div>
                            </th>
                            <th
                                className="p-4 cursor-pointer hover:text-white transition-colors text-right"
                                onClick={() => requestSort('mean_ppm')}
                            >
                                <div className="flex items-center justify-end gap-2">
                                    Mean Mercury (PPM)
                                    <ArrowUpDown className="w-4 h-4" />
                                </div>
                            </th>
                            <th className="p-4 text-right">Range (PPM)</th>
                            <th className="p-4 text-center">Safety Level</th>
                        </tr>
                    </thead>
                    <tbody className="text-slate-300 divide-y divide-white/5">
                        {sortedData.map((item, index) => {
                            const level = getMercuryLevel(item.mean_val);
                            const LevelIcon = item.mean_val < 0.15 ? ShieldCheck : (item.mean_val < 0.46 ? Info : AlertTriangle);

                            return (
                                <tr key={index} className="hover:bg-white/5 transition-colors group">
                                    <td className="p-4 font-medium text-white group-hover:text-accent-teal transition-colors">
                                        {item.species}
                                    </td>
                                    <td className="p-4 text-right font-mono text-slate-400">
                                        {item.mean_ppm}
                                    </td>
                                    <td className="p-4 text-right text-xs text-slate-500">
                                        {item.range_ppm}
                                    </td>
                                    <td className="p-4">
                                        <div className={`flex items-center justify-center gap-2 px-3 py-1 rounded-full text-xs font-bold ${level.bg} ${level.color} w-fit mx-auto`}>
                                            <LevelIcon className="w-3 h-3" />
                                            {level.label}
                                        </div>
                                    </td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
                {sortedData.length === 0 && (
                    <div className="text-center p-8 text-slate-500">
                        No species found matching "{searchTerm}"
                    </div>
                )}
            </div>
            <div className="mt-4 text-xs text-slate-600 text-center">
                Data Source: FDA (1990-2012)
            </div>
        </div>
    );
};

export default FishTable;
