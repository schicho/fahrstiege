const ENDPOINT = "https://www.wienerlinien.at/ogd_realtime/trafficInfoList?name=fahrtreppeninfo";
const FILE = "wl-current.json";

const METRO_LINES = ["U1", "U2", "U3", "U4", "U5", /* future proofing lol */ "U6"];

function getOverviewContainer() {
    return document.getElementById("wl");
}

async function fetchData() {
    try {
        const response = await fetch(FILE);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}


async function filterData(data) {
    if (!data) return [];

    let items = data.data.trafficInfos;
    let filteredItems = items.filter(item => {
        return METRO_LINES.some(line => item.relatedLines?.includes(line));
    });

    return filteredItems;
}

async function transformData(data) {
    if (!data) return [];

    return data.map(item => {
        return {
            id: item.name,
            title: item.title,
            description: item.description ? item.description : null,
            lines: item.relatedLines && item.relatedLines.length ? item.relatedLines : [],
            status: item.attributes?.status ? item.attributes.status : null,
            reason: item.attributes?.reason ? item.attributes.reason : null,
        };
    });
}

async function groupByLine(data) {
    if (!data) return {};

    let map = {};
    data.forEach(item => {
        const lines = item.lines && item.lines.length ? item.lines : ["N/A"];

        lines.forEach(line => {
            if (!map[line]) {
                map[line] = [];
            }
            map[line].push(item);
        });
    });

    return map;
}

function renderOverview(groupedData) {
    const container = getOverviewContainer();

    if (!container) {
        return;
    }

    container.innerHTML = "";

    METRO_LINES.forEach(line => {
        const lineItems = groupedData[line] || [];

        if (lineItems.length === 0) {
            return;
        }

        const card = document.createElement("div");
        card.className = "metro-card";
        card.classList.add(`metro-card--${line.toLowerCase()}`);

        const heading = document.createElement("h3");
        heading.textContent = line;
        card.appendChild(heading);

        const list = document.createElement("ul");
        list.className = "metro-card-list";

        lineItems.forEach(item => {
            const listItem = document.createElement("li");
            listItem.textContent = item.title;
            if (item.description && item.reason) {
                listItem.title = item.reason + "\n\n" + item.description;
            }
            list.appendChild(listItem);
        });

        card.appendChild(list);
        container.appendChild(card);
    });
}

function loadCounterData() {
    try {
        const response = fetch("counter.json");
        const data = response.then(res => res.json());
        return data;
    } catch (error) {
        console.error("Error loading counter data:", error);
        return null;
    }

}

function renderCounter(counterData) {
    const counterContainer = document.getElementById("counter");

    if (!counterContainer) {
        return;
    }

    counterContainer.innerHTML = "";

    // only render Karlsplatz for now, but this can be easily extended in the future
    const karlsplatzData = counterData["Karlsplatz"];
    if (karlsplatzData) {
        const countDigitsElement = document.createElement("p");
        countDigitsElement.className = "counter-digits";
        countDigitsElement.textContent = karlsplatzData.count;

        const countTextElement = document.createElement("p");
        countTextElement.className = "counter-text";
        countTextElement.textContent = `days since last breakdown (last updated: ${karlsplatzData.last_updated})`;
        counterContainer.appendChild(countDigitsElement);
        counterContainer.appendChild(countTextElement);
    }
}


(async () => {
    const data = await fetchData();
    const filteredData = await filterData(data);
    const transformedData = await transformData(filteredData);
    const groupedData = await groupByLine(transformedData);
    const counterData = await loadCounterData();

    renderOverview(groupedData);
    renderCounter(counterData);

})();
