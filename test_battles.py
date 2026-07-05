#!/usr/bin/env python3
"""
Script de prueba para el sistema de scheduler de batallas.
Ejecutar después de que el servidor esté corriendo.

Ejemplo:
    python test_battles.py http://localhost:8000 your_admin_token
"""

import httpx
import asyncio
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"
ADMIN_TOKEN = None  # Se pasa como argumento

async def test_battles():
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"} if ADMIN_TOKEN else {}
        
        print("🧪 TESTING BATTLE SCHEDULER\n")
        
        # 1. Ver info del scheduler
        print("1️⃣  Obteniendo configuración del scheduler...")
        resp = await client.get(f"{BASE_URL}/battles/info")
        print(f"   ✅ {resp.json()}\n")
        
        # 2. Ver tiempo hasta próxima batalla
        print("2️⃣  Obteniendo tiempo hasta próxima batalla...")
        resp = await client.get(f"{BASE_URL}/battles/time-until-next")
        battle_info = resp.json()
        print(f"   ✅ Próxima batalla en: {battle_info['minutes']}m {battle_info['seconds']%60}s")
        print(f"      Scheduled: {battle_info['next_battle_time']}\n")
        
        # 2.5 Ver cola de batallas (debug)
        print("2️⃣ .5 Ver cola de batallas programadas (DEBUG)...")
        resp = await client.get(f"{BASE_URL}/battles/queue")
        queue_info = resp.json()
        print(f"   ✅ Batallas en cola: {queue_info['queue_size']}")
        for battle in queue_info['battles']:
            status = "✓ executed" if battle['executed'] else "⏳ pending"
            recurring = "(recurrent)" if battle['is_recurring'] else "(one-time)"
            print(f"      #{battle['id']} {status} {recurring} @ {battle['scheduled_time']}\n")
        
        # 3. Programar batalla adicional (requiere admin)
        if ADMIN_TOKEN:
            print("3️⃣  Programando batalla adicional en 2 minutos...")
            resp = await client.post(
                f"{BASE_URL}/admin/battles/schedule-extra",
                json={"minutes_from_now": 2},
                headers=headers
            )
            if resp.status_code == 200:
                result = resp.json()
                print(f"   ✅ Batalla programada!")
                print(f"      ID: {result['id']}")
                print(f"      Cuando: {result['scheduled_time']}\n")
            else:
                print(f"   ❌ Error: {resp.text}\n")
            
            # 4. Ver tiempo actualizado
            print("4️⃣  Verificando tiempo hasta próxima batalla (debería ser ~2 minutos)...")
            resp = await client.get(f"{BASE_URL}/battles/time-until-next")
            battle_info = resp.json()
            print(f"   ✅ Próxima batalla en: {battle_info['minutes']}m {battle_info['seconds']%60}s")
            print(f"      Scheduled: {battle_info['next_battle_time']}\n")
            
            # 5. Cambiar intervalo (solo si quieres probar)
            print("5️⃣  Cambiando intervalo a 30 minutos...")
            resp = await client.post(
                f"{BASE_URL}/admin/battles/set-interval",
                json={"interval_minutes": 30},
                headers=headers
            )
            if resp.status_code == 200:
                result = resp.json()
                print(f"   ✅ Intervalo actualizado!")
                print(f"      Nuevo intervalo: {result['interval_minutes']} minutos\n")
            else:
                print(f"   ❌ Error: {resp.text}\n")
        else:
            print("3️⃣  Saltando pruebas de admin (no token proporcionado)\n")
        
        print("✅ TODAS LAS PRUEBAS COMPLETADAS!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    if len(sys.argv) > 2:
        ADMIN_TOKEN = sys.argv[2]
    else:
        print("⚠️  Sin token de admin - algunas pruebas serán saltadas")
    
    print(f"📡 Usando servidor: {BASE_URL}\n")
    asyncio.run(test_battles())
