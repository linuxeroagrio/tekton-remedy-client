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

```
oc kustomize -k fake-remedy/resources/overlays/devel | oc apply -f -
```

## Deploy del Adapter de Remedy

```
oc kustomize -k remedy-adapter/resources/overlays/devel | oc apply -f -
```

## Qué prueba esto

- Login
- Creación de CRQ
- Adjuntos
- Aprobaciones
- Tareas
- Cierre del CRQ
- Errores simulados
- Delays simulados
- Cambio automático de estado

Ideal para validar Tekton, CI/CD o integraciones sin un Remedy real.