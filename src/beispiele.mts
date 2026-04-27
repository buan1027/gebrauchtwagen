// Copyright (C) 2025 - present Juergen Zimmermann, Hochschule Karlsruhe
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

// Aufruf:  bun i
//          bun --env-file=.env prisma generate
//
//          bun --env-file=.env src\beispiele.mts

import process from 'node:process';
import { styleText } from 'node:util';
import { PrismaPg } from '@prisma/adapter-pg';
import { prismaQueryInsights } from '@prisma/sqlcommenter-query-insights';
import {
    PrismaClient,
    type Gebrauchtwagen,
    type Prisma,
} from './generated/prisma/client.ts';

let message = styleText(['black', 'bgWhite'], 'Node version');
console.log(`${message}=${process.version}`);
message = styleText(['black', 'bgWhite'], 'DATABASE_URL');
console.log(`${message}=${process.env['DATABASE_URL']}`);
console.log();

// "named parameter" durch JSON-Objekt
const adapter = new PrismaPg({
    connectionString: process.env['DATABASE_URL'],
});

// union type
const log: (Prisma.LogLevel | Prisma.LogDefinition)[] = [
    {
        // siehe unten: prisma.$on('query', ...);
        emit: 'event',
        level: 'query',
    },
    'info',
    'warn',
    'error',
];

// PrismaClient passend zur Umgebungsvariable DATABASE_URL in ".env"
// d.h. mit PostgreSQL-User "buch" und Schema "buch"
const prisma = new PrismaClient({
    // shorthand property
    adapter,
    errorFormat: 'pretty',
    log,
    comments: [prismaQueryInsights()],
});
prisma.$on('query', (e) => {
    message = styleText('green', `Query: ${e.query}`);
    console.log(message);
    message = styleText('cyan', `Duration: ${e.duration} ms`);
    console.log(message);
});

export type GebrauchtwagenMitDetails = Prisma.GebrauchtwagenGetPayload<{
    include: {
        standort: true;
        schaeden: true;
        hauptuntersuchung: true;
    };
}>;

// Operationen mit dem Model "Gebrauchtwagen"
try {
    await prisma.$connect();

    // Das Resultat ist null, falls kein Datensatz gefunden
    const fahrzeug: Gebrauchtwagen | null = await prisma.gebrauchtwagen.findUnique({
        where: { id: 1 },
    });
    message = styleText(['black', 'bgWhite'], 'fahrzeug');
    console.log(`${message} = %j`, fahrzeug);
    console.log();

    // SELECT * FROM gebrauchtwagen WHERE marke = 'VW'
    const fahrzeugeVW: GebrauchtwagenMitDetails[] = await prisma.gebrauchtwagen.findMany({
        where: {
            marke: {
                contains: 'VW',
            },
        },
        include: {
            standort: true,
            schaeden: true,
            hauptuntersuchung: true,
        },
    });
    message = styleText(['black', 'bgWhite'], 'fahrzeugeVW');
    console.log(`${message} = %j`, fahrzeugeVW);
    console.log();

    // higher-order function: Standorte aller Fahrzeuge
    const orte = fahrzeugeVW.map((f) => f.standort?.ort);
    message = styleText(['black', 'bgWhite'], 'orte');
    console.log(`${message} = %j`, orte);
    console.log();

    // Nur schadensfreie Fahrzeuge
    const schadenfrei = fahrzeugeVW.map((f) => f.schadenfrei);
    message = styleText(['black', 'bgWhite'], 'schadenfrei');
    console.log(`${message} = %j`, schadenfrei);
    console.log();

    // Pagination
    const fahrzeugePage2: Gebrauchtwagen[] = await prisma.gebrauchtwagen.findMany({
        skip: 5,
        take: 5,
    });
    message = styleText(['black', 'bgWhite'], 'fahrzeugePage2');
    console.log(`${message} = %j`, fahrzeugePage2);
    console.log();
} finally {
    await prisma.$disconnect();
}

// PrismaClient mit Admin-Rechten
const adapterAdmin = new PrismaPg({
    connectionString: process.env['DATABASE_URL_ADMIN'],
});
const prismaAdmin = new PrismaClient({ adapter: adapterAdmin });
try {
    const fahrzeugeAdmin: Gebrauchtwagen[] = await prismaAdmin.gebrauchtwagen.findMany({
        where: {
            schadenfrei: true,
        },
    });
    message = styleText(['black', 'bgWhite'], 'fahrzeugeAdmin (schadenfrei)');
    console.log(`${message} = ${JSON.stringify(fahrzeugeAdmin)}`);
} finally {
    await prismaAdmin.$disconnect();
}
