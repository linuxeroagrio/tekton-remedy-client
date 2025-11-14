# Fake Remedy + Tekton CRQ Lifecycle

Este repositorio contiene:

- Servidor fake de Remedy basado en WireMock
- Tasks Tekton
- Pipeline completo para gestionar el ciclo CRQ
- Simulación de workflow automático

## Dependencias

- OpenShift Cluster 4x
- OpenShift Pipelines Operator
- oc CLI
- tkn CLI
- Usuario con rol `cluster-admin`

## Deploy del Fake Remedy

```bash
oc kustomize -k fake-remedy/resources/overlays/devel | oc apply -f -
```

## Deploy del Adapter de Remedy

```bash
oc kustomize -k remedy-adapter/resources/overlays/devel | oc apply -f -
```

## Deploy de recursos tekton

```bash
oc kustomize -k remedy-adapter/resources/overlays/devel | oc apply -f -
```

## Pruebas

### Simulación de creación de CRQ por ejecución de tarea

## Deploy del Adapter de Remedy

```bash
tkn task start create-crq -n ci-cd \
--param ADAPTER_URL=https://$(oc get routes -n remedy-adapter remedy-adapter -o jsonpath='{.status.ingress[0].host}') \
--param DESCRIPTION="Actualización de sistema en servidor de aplicaciones" \
--param DETAILED_DESCRIPTION="Se aplicarán parches de seguridad y se reiniciará el servicio." \
--param IMPACT=4-Minor/Localized \
--param URGENCY=3-Medium \
--param RISK_LEVEL=Moderate \
--param SUMMARY=Mantenimiento de seguridad \
--param CATEGORIZATION_TIER_1=Infrastructure \
--param CATEGORIZATION_TIER_2=Servers \
--param CATEGORIZATION_TIER_3=Patching \
--param PRODUCT_CATEGORIZATION_TIER_1=Hardware \
--param PRODUCT_CATEGORIZATION_TIER_2=Servers \
--param PRODUCT_CATEGORIZATION_TIER_3=Linux \
--param OPERATIONAL_CATEGORIZATION_TIER_1=Maintenance \
--param OPERATIONAL_CATEGORIZATION_TIER_2=Scheduled \
--param REPORTED_SOURCE="Automated System" \
--param REQUESTER_ID=svc-tekton \
--param ASSIGNED_GROUP="Change Management" \
--param ASSIGNEE=auto-assign \
--param STATUS=Draft \
--use-param-defaults \
--showlog
```

## Qué prueba esto

- Login
- Creación de CRQ
- Adjuntos
- Aprobaciones
- Tareas
- Cierre del CRQ

Creado para validar Tekton, CI/CD o integraciones sin un Remedy real.