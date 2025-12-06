const { useState, useEffect } = React;

function App() {
    const [activeTab, setActiveTab] = useState('races');
    const [data, setData] = useState({});
    const [loading, setLoading] = useState(true);
    const [selectedItem, setSelectedItem] = useState(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const tabs = ['races', 'classes', 'spells', 'monsters'];
            const loadedData = {};
            
            for (const tab of tabs) {
                try {
                    const response = await fetch(`dnd_raw/${tab}.json`);
                    if (response.ok) {
                        const json = await response.json();
                        loadedData[tab] = json.results || [];
                    }
                } catch (e) {
                    console.error(`Failed to load ${tab}:`, e);
                    loadedData[tab] = [];
                }
            }
            
            setData(loadedData);
            setLoading(false);
        } catch (error) {
            console.error('Error loading data:', error);
            setLoading(false);
        }
    };

    const handleItemClick = async (item, tab) => {
        try {
            const fileName = `dnd_raw/${tab}_${item.index.replace('/', '_')}.json`;
            const response = await fetch(fileName);
            if (response.ok) {
                const details = await response.json();
                setSelectedItem({ ...details, type: tab });
            } else {
                setSelectedItem({ ...item, type: tab });
            }
        } catch (e) {
            setSelectedItem({ ...item, type: tab });
        }
    };

    if (loading) {
        return React.createElement('div', {
            className: 'min-h-screen bg-gray-900 text-white flex items-center justify-center'
        }, React.createElement('div', { className: 'text-xl' }, 'Loading D&D data...'));
    }

    return React.createElement('div', { className: 'min-h-screen bg-gray-900 text-white' },
        React.createElement('header', { className: 'bg-gray-800 border-b border-gray-700 p-4' },
            React.createElement('h1', { className: 'text-3xl font-bold' }, 'D&D 5e Data Viewer')
        ),
        React.createElement('div', { className: 'flex' },
            React.createElement('aside', { className: 'w-64 bg-gray-800 border-r border-gray-700 p-4' },
                React.createElement('nav', { className: 'space-y-2' },
                    ['races', 'classes', 'spells', 'monsters'].map(tab =>
                        React.createElement('button', {
                            key: tab,
                            onClick: () => {
                                setActiveTab(tab);
                                setSelectedItem(null);
                            },
                            className: `w-full text-left px-4 py-2 rounded ${
                                activeTab === tab
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                            }`
                        }, tab.charAt(0).toUpperCase() + tab.slice(1))
                    )
                )
            ),
            React.createElement('main', { className: 'flex-1 p-6' },
                selectedItem
                    ? React.createElement('div', null,
                        React.createElement('button', {
                            onClick: () => setSelectedItem(null),
                            className: 'mb-4 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded'
                        }, '← Back'),
                        React.createElement(ItemDetails, { item: selectedItem })
                    )
                    : React.createElement(ItemList, {
                        items: data[activeTab] || [],
                        tab: activeTab,
                        onItemClick: handleItemClick
                    })
            )
        )
    );
}

function ItemList({ items, tab, onItemClick }) {
    if (!items || items.length === 0) {
        return React.createElement('div', { className: 'text-gray-400' },
            `No ${tab} data available.`
        );
    }

    return React.createElement('div', null,
        React.createElement('h2', { className: 'text-2xl font-bold mb-4 capitalize' },
            `${tab} (${items.length})`
        ),
        React.createElement('div', { className: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' },
            items.map((item, idx) =>
                React.createElement('div', {
                    key: idx,
                    onClick: () => onItemClick(item, tab),
                    className: 'bg-gray-800 p-4 rounded-lg cursor-pointer hover:bg-gray-700 border border-gray-700'
                },
                    React.createElement('h3', { className: 'font-semibold text-lg' }, item.name),
                    item.level !== undefined && React.createElement('p', { className: 'text-gray-400 text-sm' },
                        `Level ${item.level}`
                    )
                )
            )
        )
    );
}

function ItemDetails({ item }) {
    const renderValue = (value) => {
        if (value === null || value === undefined) return null;
        if (typeof value === 'object') {
            if (Array.isArray(value)) {
                return React.createElement('ul', { className: 'list-disc list-inside ml-4' },
                    value.map((v, i) =>
                        React.createElement('li', { key: i },
                            typeof v === 'object' ? JSON.stringify(v) : String(v)
                        )
                    )
                );
            }
            return React.createElement('pre', {
                className: 'bg-gray-800 p-2 rounded text-sm overflow-x-auto'
            }, JSON.stringify(value, null, 2));
        }
        return React.createElement('span', null, String(value));
    };

    const entries = Object.entries(item)
        .filter(([key]) => key !== 'name' && key !== 'index' && key !== 'type');

    return React.createElement('div', { className: 'bg-gray-800 rounded-lg p-6 border border-gray-700' },
        React.createElement('h2', { className: 'text-3xl font-bold mb-4' },
            item.name || item.index
        ),
        React.createElement('div', { className: 'space-y-4' },
            entries.map(([key, value]) =>
                React.createElement('div', { key: key },
                    React.createElement('h3', { className: 'font-semibold text-lg capitalize mb-1' },
                        key.replace(/_/g, ' ')
                    ),
                    React.createElement('div', { className: 'text-gray-300 ml-4' },
                        renderValue(value)
                    )
                )
            )
        )
    );
}

ReactDOM.render(React.createElement(App), document.getElementById('root'));


